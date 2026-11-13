import { Bar, Button, Check, Roll, Stage, Text, Window, type Act } from '../../kit'
import './hero.css'

// Free AI: a guest presses play on a lesson, signs up with Google in one
// step, the lesson plays, and is marked done; the course progress moves.

type S = { signup: boolean; playing: boolean; progress: number; done: boolean; count: number }

const initial: S = { signup: false, playing: false, progress: 0, done: false, count: 2 }
const POSTER: S = { signup: false, playing: true, progress: 1, done: true, count: 3 }

const LESSONS = ['מה זה Claude', 'איך מבקשים נכון', 'פרויקטים וקבצים']

async function script(a: Act<S>) {
  await a.wait(700)
  await a.move('play')
  await a.wait(250)
  await a.click()
  await a.set({ signup: true })
  await a.wait(900)
  await a.move('google')
  await a.wait(250)
  await a.click()
  await a.set({ signup: false })
  await a.wait(250)
  await a.set({ playing: true, progress: 1 })
  await a.move('rest')
  await a.wait(2600)
  await a.move('done')
  await a.wait(250)
  await a.click()
  await a.set({ done: true, count: 3 })
  await a.move('rest')
  await a.wait(2600)
  await a.set({ ...initial })
  await a.wait(600)
}

export function FreeAiHero() {
  return (
    <Stage
      width={720}
      height={440}
      compact={{ below: 600, width: 358, height: 440 }}
      initial={initial}
      poster={POSTER}
      script={script}
      cursor={{ at: { wide: { x: 560, y: 300 }, compact: { x: 250, y: 330 } }, ripple: true }}
      className="fa"
    >
      {(s, _rect, layout) => (
        <>
          <Window url="free-ai.co.il" urlShape="pill" className="fa-win">
            <div className="fa-page" dir="rtl">
              <main className="fa-main">
                <div className="fa-kicker">Claude מאפס · שיעור 3</div>
                <div className="fa-title">פרויקטים וקבצים</div>
                <div className="fa-video" data-playing={s.playing || undefined}>
                  <div className="fa-video-art" />
                  <div className="fa-slide" data-show={s.playing || undefined}>
                    <div className="fa-slide-k">שיעור 3</div>
                    <div className="fa-slide-t">כל הקבצים במקום אחד.</div>
                    <div className="fa-slide-bars"><Bar w={180} h={7} tone={1} /><Bar w={140} h={7} tone={1} /><Bar w={160} h={7} tone={1} /></div>
                  </div>
                  <span className="fa-play" data-target="play" data-cursor="pointer" data-hide={s.playing || undefined}>
                    <svg width="18" height="18" viewBox="0 0 24 24" aria-hidden><path d="M8 5v14l11-7z" fill="currentColor" /></svg>
                  </span>
                  <div className="fa-track"><div className="fa-fill" style={{ transform: `scaleX(${s.progress})` }} /></div>
                </div>
                <div className="fa-actions">
                  <Button data-target="done" variant={s.done ? 'secondary' : 'primary'} icon={s.done ? <Check on size={14} /> : undefined} className="fa-done">
                    {s.done ? 'הושלם' : 'סיימתי את השיעור'}
                  </Button>
                  <span className="fa-next">השיעור הבא ‹</span>
                </div>
              </main>
              {layout === 'wide' && (
                <aside className="fa-side">
                  <div className="fa-side-head">
                    <span>שיעורים</span>
                    <span className="fa-count"><Roll>{String(s.count)}</Roll><span>מתוך 12</span></span>
                  </div>
                  {LESSONS.map((t, i) => {
                    const on = i < 2 || (i === 2 && s.done)
                    return (
                      <div key={t} className="fa-lesson" data-current={i === 2 || undefined}>
                        <Check on={on} size={16} />
                        <Text className="fa-lesson-t">{t}</Text>
                      </div>
                    )
                  })}
                  {[70, 52, 64].map((w, i) => (
                    <div key={i} className="fa-lesson">
                      <Check on={false} size={16} />
                      <Bar w={w} h={6} tone={2} />
                    </div>
                  ))}
                </aside>
              )}
            </div>
          </Window>

          <div className="fa-signup" data-show={s.signup || undefined} dir="rtl">
            <div className="fa-signup-title">נרשמים וצופים. בחינם.</div>
            <div className="fa-signup-sub">ואתם חוזרים בדיוק לשיעור הזה</div>
            <span className="fa-google" data-target="google" data-cursor="pointer">
              <svg width="16" height="16" viewBox="0 0 48 48" aria-hidden><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.6l6.8-6.8C35.8 2.4 30.3 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.1C12.4 13.6 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.1 24.5c0-1.6-.1-3.1-.4-4.5H24v9h12.4c-.5 2.9-2.2 5.3-4.6 6.9l7.4 5.8c4.3-4 6.9-9.9 6.9-17.2z"/><path fill="#FBBC05" d="M10.5 28.6c-.5-1.4-.8-3-.8-4.6s.3-3.2.8-4.6l-7.9-6.1C.9 16.6 0 20.2 0 24s.9 7.4 2.6 10.7l7.9-6.1z"/><path fill="#34A853" d="M24 48c6.5 0 11.9-2.1 15.8-5.8l-7.4-5.8c-2.1 1.4-4.8 2.2-8.4 2.2-6.3 0-11.6-4.1-13.5-9.8l-7.9 6.1C6.6 42.6 14.6 48 24 48z"/></svg>
              המשך עם Google
            </span>
          </div>
          <span data-target="rest" style={{ position: 'absolute', left: layout === 'wide' ? 560 : 250, top: layout === 'wide' ? 300 : 330 }} />
        </>
      )}
    </Stage>
  )
}
