// גיבוי יומי של כל הפרויקטים מכל חשבונות ה-GitHub ל-Google Drive.
// שמים כאן מפתח אחד לכל חשבון GitHub (בין המירכאות, מופרדים בפסיק).
const TOKENS = [
  'PASTE_TOKEN_ACCOUNT_1',
  // 'PASTE_TOKEN_ACCOUNT_2',
];

const ROOT_FOLDER = 'GitHub Backups';
const RUN_HOUR = 3; // שעת הריצה היומית
const MAX_RUN_MS = 4.5 * 60 * 1000;

// להריץ פעם אחת בלבד: יוצר את התזמון היומי ומריץ גיבוי ראשון.
function setup() {
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('backupAll').timeBased().everyDays(1).atHour(RUN_HOUR).create();
  backupAll();
}

function backupAll() {
  const start = Date.now();
  const props = PropertiesService.getScriptProperties();
  const root = getFolder_(DriveApp.getRootFolder(), ROOT_FOLDER);

  let queue = readQueue_(root);
  if (!queue) queue = buildQueue_();

  while (queue.length) {
    if (Date.now() - start > MAX_RUN_MS) {
      writeQueue_(root, queue);
      ScriptApp.newTrigger('continueBackup').timeBased().after(60 * 1000).create();
      return;
    }
    const item = queue.shift();
    try {
      backupRepo_(root, item, props);
    } catch (e) {
      console.log('נכשל: ' + item.name + ' — ' + e);
    }
  }
  writeQueue_(root, null);
  props.setProperty('lastRun', new Date().toISOString());
}

function continueBackup() {
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'continueBackup')
    .forEach(t => ScriptApp.deleteTrigger(t));
  backupAll();
}

function buildQueue_() {
  const queue = [];
  TOKENS.forEach((token, t) => {
    if (!token || token.indexOf('PASTE_') === 0) return;
    let page = 1;
    while (true) {
      const res = gh_(token, 'https://api.github.com/user/repos?affiliation=owner&per_page=100&page=' + page);
      if (res.getResponseCode() !== 200) {
        console.log('נכשל: מפתח מספר ' + (t + 1) + ' — ' + res.getContentText());
        break;
      }
      const repos = JSON.parse(res.getContentText());
      repos.forEach(r => queue.push({ t: t, name: r.full_name, pushed: r.pushed_at }));
      if (repos.length < 100) break;
      page++;
    }
  });
  return queue;
}

function backupRepo_(root, item, props) {
  const key = 'p:' + item.name;
  const [owner, repo] = item.name.split('/');
  const folder = getFolder_(root, owner);
  const fileName = repo + '.zip';
  const exists = folder.getFilesByName(fileName).hasNext();
  if (exists && props.getProperty(key) === item.pushed) return; // לא השתנה מאז הגיבוי הקודם

  const res = gh_(TOKENS[item.t], 'https://api.github.com/repos/' + item.name + '/zipball');
  if (res.getResponseCode() !== 200) {
    console.log('דילוג: ' + item.name + ' (' + res.getResponseCode() + ')');
    return;
  }
  const blob = res.getBlob().setName(fileName);
  const old = folder.getFilesByName(fileName);
  while (old.hasNext()) old.next().setTrashed(true);
  folder.createFile(blob);
  props.setProperty(key, item.pushed);
}

function gh_(token, url) {
  return UrlFetchApp.fetch(url, {
    headers: { Authorization: 'Bearer ' + token, Accept: 'application/vnd.github+json' },
    muteHttpExceptions: true,
  });
}

function getFolder_(parent, name) {
  const it = parent.getFoldersByName(name);
  return it.hasNext() ? it.next() : parent.createFolder(name);
}

function readQueue_(root) {
  const it = root.getFilesByName('_queue.json');
  return it.hasNext() ? JSON.parse(it.next().getBlob().getDataAsString()) : null;
}

function writeQueue_(root, queue) {
  const it = root.getFilesByName('_queue.json');
  while (it.hasNext()) it.next().setTrashed(true);
  if (queue) root.createFile('_queue.json', JSON.stringify(queue), 'application/json');
}
