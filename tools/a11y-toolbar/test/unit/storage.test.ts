import { afterEach, describe, expect, it, vi } from 'vitest';
import { DEFAULT_STORAGE_KEY, StorageManager, SyncManager, parseStored, serialize } from '../../src/managers/StorageManager';
import { defaultPreferences } from '../../src/preferences';
import type { AccessibilityPreferences } from '../../src/types';

const sample: AccessibilityPreferences = { ...defaultPreferences, textScale: 1.2, highlightLinks: true };

afterEach(() => {
  localStorage.clear();
  vi.unstubAllGlobals();
});

describe('parseStored', () => {
  it('handles empty, invalid JSON and corrupted objects', () => {
    expect(parseStored(null)).toEqual(defaultPreferences);
    expect(parseStored('{not json')).toEqual(defaultPreferences);
    expect(parseStored('[]')).toEqual(defaultPreferences);
    expect(parseStored('{"version":1,"preferences":"x"}')).toEqual(defaultPreferences);
  });

  it('reads the current schema and keeps only valid fields', () => {
    const raw = JSON.stringify({ version: 1, preferences: { ...sample, textScale: 7, extra: true } });
    const result = parseStored(raw);
    expect(result.textScale).toBe(1);
    expect(result.highlightLinks).toBe(true);
    expect('extra' in result).toBe(false);
  });

  it('migrates the unversioned format and ignores unknown future versions', () => {
    expect(parseStored(JSON.stringify({ readableFont: true })).readableFont).toBe(true);
    expect(parseStored(JSON.stringify({ version: 99, preferences: sample }))).toEqual(defaultPreferences);
  });

  it('round-trips through serialize', () => {
    expect(parseStored(serialize(sample))).toEqual(sample);
  });
});

describe('StorageManager', () => {
  it('uses the versioned default key and clears only its own key', () => {
    localStorage.setItem('host-app', 'keep me');
    const storage = new StorageManager(window);
    expect(storage.key).toBe(DEFAULT_STORAGE_KEY);
    storage.save(sample);
    expect(JSON.parse(localStorage.getItem(DEFAULT_STORAGE_KEY) ?? '{}')).toMatchObject({ version: 1 });
    expect(storage.load()).toEqual(sample);
    storage.clear();
    expect(localStorage.getItem(DEFAULT_STORAGE_KEY)).toBeNull();
    expect(localStorage.getItem('host-app')).toBe('keep me');
  });

  it('falls back to memory when localStorage throws', () => {
    const throwing = {
      get localStorage(): Storage {
        throw new Error('SecurityError');
      },
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
    } as unknown as Window;
    const storage = new StorageManager(throwing);
    expect(storage.persistent).toBe(false);
    storage.save(sample);
    expect(storage.load()).toEqual(sample);
    expect(storage.onExternalChange(vi.fn())).toBeTypeOf('function');
  });

  it('works without a window at all', () => {
    const storage = new StorageManager(null);
    storage.save(sample);
    expect(storage.load()).toEqual(sample);
  });

  it('reports writes from other tabs through the storage event', () => {
    const storage = new StorageManager(window);
    const handler = vi.fn();
    const stop = storage.onExternalChange(handler);
    window.dispatchEvent(new StorageEvent('storage', { key: DEFAULT_STORAGE_KEY, newValue: serialize(sample) }));
    window.dispatchEvent(new StorageEvent('storage', { key: 'other', newValue: 'x' }));
    expect(handler).toHaveBeenCalledOnce();
    expect(handler).toHaveBeenCalledWith(sample);
    stop();
    window.dispatchEvent(new StorageEvent('storage', { key: DEFAULT_STORAGE_KEY, newValue: null }));
    expect(handler).toHaveBeenCalledOnce();
  });
});

/** In-process BroadcastChannel stand-in that delivers to every other instance with the same name. */
class FakeChannel {
  static readonly all = new Set<FakeChannel>();
  onmessage: ((event: MessageEvent<unknown>) => void) | null = null;
  constructor(readonly name: string) {
    FakeChannel.all.add(this);
  }
  postMessage(data: unknown): void {
    for (const other of FakeChannel.all) {
      if (other !== this && other.name === this.name) other.onmessage?.({ data } as MessageEvent<unknown>);
    }
  }
  close(): void {
    FakeChannel.all.delete(this);
  }
}

describe('SyncManager', () => {
  it('syncs through BroadcastChannel and ignores its own messages', () => {
    vi.stubGlobal('BroadcastChannel', FakeChannel);
    const storage = new StorageManager(window);
    const receivedA = vi.fn();
    const receivedB = vi.fn();
    const a = new SyncManager(window, storage, receivedA);
    const b = new SyncManager(window, storage, receivedB);
    a.start();
    b.start();
    expect(a.mode).toBe('broadcast');
    a.publish(sample);
    expect(receivedB).toHaveBeenCalledWith(sample);
    expect(receivedA).not.toHaveBeenCalled();
    a.stop();
    b.stop();
    expect(FakeChannel.all.size).toBe(0);
  });

  it('falls back to the storage event when BroadcastChannel is unavailable', () => {
    vi.stubGlobal('BroadcastChannel', undefined);
    const storage = new StorageManager(window);
    const received = vi.fn();
    const sync = new SyncManager(window, storage, received);
    sync.start();
    expect(sync.mode).toBe('storage');
    window.dispatchEvent(new StorageEvent('storage', { key: DEFAULT_STORAGE_KEY, newValue: serialize(sample) }));
    expect(received).toHaveBeenCalledWith(sample);
    sync.stop();
  });

  it('continues without sync when nothing is available', () => {
    const sync = new SyncManager(null, new StorageManager(null), vi.fn());
    sync.start();
    expect(sync.mode).toBe('none');
    expect(() => sync.publish(sample)).not.toThrow();
    sync.stop();
  });

  it('ignores malformed messages', () => {
    vi.stubGlobal('BroadcastChannel', FakeChannel);
    const received = vi.fn();
    const sync = new SyncManager(window, new StorageManager(window), received);
    sync.start();
    const sender = new FakeChannel(`a11y-toolbar:${DEFAULT_STORAGE_KEY}`);
    sender.postMessage({ hello: 'world' });
    sender.postMessage({ namespace: 'a11y-toolbar', version: 2, source: 'x', preferences: sample });
    expect(received).not.toHaveBeenCalled();
    sender.close();
    sync.stop();
  });
});
