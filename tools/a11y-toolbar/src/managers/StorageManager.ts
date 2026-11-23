import { defaultPreferences, isRecord, sanitizePreferences } from '../preferences';
import type { AccessibilityPreferences, StoredPreferencesV1, SyncMessage, Unsubscribe } from '../types';
import { createId } from '../utils/browser';

export const DEFAULT_STORAGE_KEY = 'a11y-toolbar-preferences-v1';
export const SCHEMA_VERSION = 1;

/** Reads a stored payload of any supported schema version. Unsupported or broken data yields defaults. */
export function parseStored(raw: string | null): AccessibilityPreferences {
  if (raw === null || raw === '') return defaultPreferences;
  let data: unknown;
  try {
    data = JSON.parse(raw);
  } catch {
    return defaultPreferences;
  }
  if (!isRecord(data)) return defaultPreferences;
  const version = data.version;
  if (version === SCHEMA_VERSION) return sanitizePreferences(data.preferences);
  // Version 0: an unversioned flat preferences object.
  if (version === undefined) return sanitizePreferences(data);
  return defaultPreferences;
}

export function serialize(preferences: AccessibilityPreferences): string {
  const payload: StoredPreferencesV1 = { version: SCHEMA_VERSION, preferences };
  return JSON.stringify(payload);
}

function getLocalStorage(win: Window | null): Storage | null {
  if (!win) return null;
  try {
    const storage = win.localStorage;
    const probe = '__a11y-toolbar-probe__';
    storage.setItem(probe, probe);
    storage.removeItem(probe);
    return storage;
  } catch {
    return null;
  }
}

/** Persists preferences under one versioned key. Falls back to memory when localStorage is unavailable. */
export class StorageManager {
  private readonly storage: Storage | null;
  private memory: string | null = null;

  constructor(private readonly win: Window | null, readonly key: string = DEFAULT_STORAGE_KEY) {
    this.storage = getLocalStorage(win);
  }

  get persistent(): boolean {
    return this.storage !== null;
  }

  load(): AccessibilityPreferences {
    if (!this.storage) return parseStored(this.memory);
    try {
      return parseStored(this.storage.getItem(this.key));
    } catch {
      return parseStored(this.memory);
    }
  }

  save(preferences: AccessibilityPreferences): void {
    const value = serialize(preferences);
    this.memory = value;
    if (!this.storage) return;
    try {
      this.storage.setItem(this.key, value);
    } catch {
      /* Quota or privacy mode: the in-memory copy keeps the session working. */
    }
  }

  clear(): void {
    this.memory = null;
    if (!this.storage) return;
    try {
      this.storage.removeItem(this.key);
    } catch {
      /* Nothing else to clean. */
    }
  }

  /** Watches writes made by other tabs. Used only when BroadcastChannel is missing. */
  onExternalChange(handler: (prefs: AccessibilityPreferences) => void): Unsubscribe {
    const win = this.win;
    if (!win || !this.storage) return () => undefined;
    const listener = (event: StorageEvent): void => {
      if (event.key !== this.key && event.key !== null) return;
      handler(event.key === null ? defaultPreferences : parseStored(event.newValue));
    };
    win.addEventListener('storage', listener);
    return () => win.removeEventListener('storage', listener);
  }
}

function isSyncMessage(value: unknown): value is SyncMessage {
  return isRecord(value) && value.namespace === 'a11y-toolbar' && value.version === SCHEMA_VERSION
    && typeof value.source === 'string' && isRecord(value.preferences);
}

/** Cross-tab synchronization: BroadcastChannel first, the storage event second, nothing as the last resort. */
export class SyncManager {
  readonly source = createId();
  private channel: BroadcastChannel | null = null;
  private stopStorage: Unsubscribe = () => undefined;

  constructor(
    private readonly win: Window | null,
    private readonly storage: StorageManager,
    private readonly onRemote: (prefs: AccessibilityPreferences) => void,
  ) {}

  get mode(): 'broadcast' | 'storage' | 'none' {
    if (this.channel) return 'broadcast';
    return this.storage.persistent && this.win ? 'storage' : 'none';
  }

  start(): void {
    const Channel: typeof BroadcastChannel | undefined = this.win
      ? (this.win as Window & { BroadcastChannel?: typeof BroadcastChannel }).BroadcastChannel
      : undefined;
    if (typeof Channel === 'function') {
      try {
        const channel = new Channel(`a11y-toolbar:${this.storage.key}`);
        channel.onmessage = (event: MessageEvent<unknown>) => {
          const data = event.data;
          if (!isSyncMessage(data) || data.source === this.source) return;
          this.onRemote(sanitizePreferences(data.preferences));
        };
        this.channel = channel;
        return;
      } catch {
        this.channel = null;
      }
    }
    this.stopStorage = this.storage.onExternalChange(this.onRemote);
  }

  publish(preferences: AccessibilityPreferences): void {
    if (!this.channel) return;
    const message: SyncMessage = { namespace: 'a11y-toolbar', version: SCHEMA_VERSION, source: this.source, preferences };
    try {
      this.channel.postMessage(message);
    } catch {
      /* A closed channel is not worth crashing for. */
    }
  }

  stop(): void {
    if (this.channel) {
      this.channel.onmessage = null;
      this.channel.close();
      this.channel = null;
    }
    this.stopStorage();
    this.stopStorage = () => undefined;
  }
}
