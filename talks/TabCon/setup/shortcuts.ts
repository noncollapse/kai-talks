import { defineShortcutsSetup } from '@slidev/types'

export default defineShortcutsSetup((nav, shortcuts) =>
  // Some presentation remotes send Up/Down. Slidev normally skips all reveals
  // for those keys; use the same stepwise navigation as Left/Right instead.
  shortcuts.map(shortcut => {
    if (shortcut.name === 'next_down')
      return { ...shortcut, fn: nav.next }
    if (shortcut.name === 'prev_up')
      return { ...shortcut, fn: nav.prev }
    return shortcut
  }),
)
