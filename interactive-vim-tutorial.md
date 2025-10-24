
# NeoVim Interactive Tutorial

Paste this whole file into a new buffer and work **inside it**. Perform each task using only the commands listed for that section. Your **leader** is assumed to be `,` (comma).

> Tips
>
> * Stay in Normal mode. Press `<Esc>` whenever you feel lost.
> * Use counts: `3w`, `5dd`, `20j`, etc.
> * Use `u` to undo and `<C-r>` to redo.
> * Use `:help {thing}` at any time. Example: `:help text-objects`.

---

## 0) Warm‑up: Modes and the dot repeat

**Goal:** Get comfortable with modes and repeating edits.

**Know for this section:**

* `i` `a` `I` `A` `o` `O` — insert variants
* `<Esc>` — back to Normal
* `.` — repeat last change
* `u` `<C-r>` — undo/redo

**Try it:**

1. Move to the lines below. Enter Insert with `i`. Type a word. `<Esc>`. Use `.` to repeat that exact insertion on the next line without retyping.
2. Use `A` to append at end of line. Undo with `u`. Redo with `<C-r>`.

```
[edit-me] starter line
[edit-me] another line
[edit-me] yet another line
```

---

## 1) Movement fundamentals

**Goal:** Cross text without arrow keys.

**Know:**

* Single steps: `h` `j` `k` `l`
* By word: `w` `b` `e` `ge` (big words: `W` `B` `E`)
* Line anchors: `0` `^` `$` `g_`
* File anchors: `gg` top, `G` bottom, `{` `}` paragraphs, `(` `)` sentences
* Screen lines: `H` `M` `L`

**Try it:**

* Jump word by word through the paragraph and land exactly on the `:` characters using `w` and `e`. Then go backwards with `b` and `ge`.

```
Vim movement practice: jump quickly; land precisely; avoid arrow keys; use counts to move faster; celebrate small wins.
```

* Go to start of this bullet using `0`, then to first non‑blank with `^`, then to line end with `$`, then last non‑blank with `g_`.

---

## 2) Find and Till within a line

**Goal:** Snipe characters on a line.

**Know:**

* `f{char}` jump **to** the char, `t{char}` jump **till** before it
* `F` `T` go leftwards
* `;` repeat, `,` repeat opposite

**Try it:**

* On the line below, place the cursor at start. Use `t;` then `;` repeatedly to hop from semicolon to semicolon. Come back with `,`.

```
alpha;beta;gamma;delta;epsilon;zeta;eta;theta
```

---

## 3) Operators + Motions = Editing

**Goal:** Combine operators with motions.

**Know:**

* Delete `d{motion}`
* Change `c{motion}` (delete + insert)
* Yank `y{motion}`
* Case: `gU{motion}` upper, `gu{motion}` lower, `~` toggle
* Indent: `>` `<` with motions or lines `>>` `<<`
* Join: `J` (keep space) `gJ` (no space)

**Try it:**

1. Change the word `wrong` to `right` using `ciw`.
2. Delete from the `[` to the `]` using `dF[` or `dt]` appropriately.
3. Uppercase the next sentence using `gU(`.

```
This is the wrong token in this line. [target] bracketed part.
Next sentence should be uppercased smoothly. keep this one unchanged.
```

---

## 4) Linewise edits

**Goal:** Work at line granularity.

**Know:**

* `dd` delete line, `cc` change line, `yy` yank line
* `D` delete to end of line, `C` change to end of line, `Y` = `yy`
* `p` `P` put after/before, `gp` `gP` place and move after text

**Try it:**

* Yank the first list item then paste it after the third using counts and `p`.
* Join the two wrapped lines into one with `J`.

```
1) apples
2) pears
3) plums
This line wraps
because it is long.
```

---

## 5) Visual selections and text objects

**Goal:** Select smarter regions.

**Know:**

* Visual: `v` (char), `V` (line), `<C-v>` (block)
* Text objects: `iw/aw` inner/a word; `i" a"`, `i' a'`, `i) a)` etc.; `ip/ap` paragraph
* Swap selection end: `o` inside Visual

**Try it:**

1. With cursor anywhere inside the quotes, delete the **inner quotes content** using `di"`.
2. Change **a** parenthesized expression with `ca)`.
3. Use block Visual `<C-v>` to add `// ` to the three code lines at column 1 using `I// <Esc>`.

```
The quick "brown fox" jumps.
Compute now (but not later).
code line one
code line two
code line three
```

---

## 6) Searching and match navigation

**Goal:** Find fast. Move between matches.

**Know:**

* Forward/backward search: `/pattern` `?pattern`
* Next/prev: `n` `N`
* Word under cursor: `*` `#` (and `g*` `g#` for partial)
* Clear highlight: `:noh`

**Try it:**

* Put cursor on the word `signal` then use `*` to jump through all matches.
* Search for `edge\s\+case` using very‑magic `\v` like `/\vedge\s+case`.

```
Edge cases signal bugs. A signal in a crowded signal field tests your search technique. Edge   case again.
```

---

## 7) Substitution and ranges

**Goal:** Replace safely.

**Know:**

* Current line: `:s/old/new/`
* Whole file: `:%s/old/new/g`
* Confirm each: add `c`
* Word boundaries: `\<` `\>`; very‑magic: `\v`
* Ranges: `:5,12s/ /_/g` or `:'<,'>s/...`

**Try it:**

* Replace all `TODO` with `DONE` across the block with confirmation.
* Replace any number sequence with `[NUM]` using `\v` and `\d+`.

```
TODO implement search
TODO write tests
TODO refactor 123 and 9876 safely
```

---

## 8) Buffers, tabs, and files

**Goal:** Navigate open files.

**Know:**

* Open/edit: `:e file`, `:edit %:h` parent dir
* List buffers: `:ls` or `:buffers`
* Next/prev buffer: `:bn` `:bp`, alternate: `Ctrl-^` (`<C-^>`) or `:b#`
* Go to buffer N: `:b {N}` or `:b {namepart}`
* Delete buffer: `:bd`
* Tabs: `:tabnew`, `gt` next `gT` prev, `:tabclose`

**Try it:**

* Open a scratch split with `:vnew`, type some text, then `:bd` to close that buffer.

---

## 9) Windows and splits

**Goal:** Tile your view.

**Know:**

* `:split` `:vsplit` or `:sp` `:vs`
* Move: `<C-w>h/j/k/l` or `<C-w>w` to cycle
* Size: `<C-w>=` equalize, `<C-w>_` max height, `<C-w>|` max width
* Close: `<C-w>q` or `:q`
* Only: `<C-w>o`

**Try it:**

* Create a vertical split, duplicate this buffer with `:vsplit | b#`, then move between panes using `<C-w>h/l`.

---

## 10) Marks and jumps

**Goal:** Teleport within the file.

**Know:**

* Set mark: `ma` (a–z)
* Jump to mark: `` `a `` exact column or `'a` to line
* Recent jumps: `<C-o>` back, `<C-i>` forward
* Marks `'` and `` ` `` for last jump, `` `. `` for last change

**Try it:**

* Set `ma` at this line. Scroll away, then jump back with `` `a ``.

---

## 11) Registers and paste control

**Goal:** Use multiple clipboards.

**Know:**

* Show: `:registers` or `:reg`
* Named: `"ayy` yanks line to register a, `"ap` pastes it
* Black hole: `"_d{motion}` to delete without yanking
* System: `"+` (clipboard) and `"*` (selection) if available

**Try it:**

* Yank a line into register `b` and paste it twice from `b` without affecting the default register.

---

## 12) Macros and repeatable edits

**Goal:** Automate a boring change.

**Know:**

* Start/stop recording: `qa` … `q`
* Play: `@a`, repeat last macro `@@`
* Use counts: `10@a`

**Try it:**

* Record a macro that converts `name: value` into `"name" = value` on a line, then apply to all lines below with a count.

```
name: 10
answer: 42
speed: 9001
```

---

## 13) Indenting and formatting

**Goal:** Clean structure.

**Know:**

* Reindent motion: `={motion}`
* Whole file: `gg=G`
* Shift lines: `>>` `<<`
* Format with `gq{motion}` (wrap text)

**Try it:**

* Reindent the code block with `gg=G` then wrap the paragraph to 72 columns with `gqap` after setting `:set textwidth=72`.

```
if (x) {
    if(y){
  doThing();}
}

This paragraph is deliberately tooooooooooooooooo long and should be wrapped by the formatter once you set the textwidth to an appropriate value and run the proper operator on the paragraph object.
```

---

## 14) Folding

**Goal:** Hide and reveal detail.

**Know:**

* Create manual fold over a motion: `zf{motion}` (e.g., `zf%`)
* Toggle: `za`, open: `zo`, close: `zc`
* All: `zR` open all, `zM` close all
* Method: `:set foldmethod=indent|marker|manual`

**Try it:**

* Fold the bracketed block with `zf%` then open/close it.

```
function demo() {
    if (true) {
        // detail
    }
}
```

---

## 15) Global, ranges, and Ex power moves

**Goal:** Operate on many lines at once.

**Know:**

* `:g/pattern/ normal >>` — run Normal on matching lines
* `:v/pattern/ d` — delete lines **not** matching
* Ranges: `:'<,'>`, `:.,.+10`, `:%`
* Sorting: `:sort` or `:sort!`

**Try it:**

* Sort the following names alphabetically then delete lines that contain digits.

```
zoe
Ada
carol2
bob
mallory3
Eve
```

---

## 16) Quickfix and grep

**Goal:** Navigate many matches.

**Know:**

* Grep in files: `:vimgrep /TODO/ **/*.md`
* Open list: `:copen` close: `:cclose`
* Move: `:cnext` `:cprev` `:clist`
* Apply a change to all items using `:cfdo` (careful; read `:help :cfdo`)

**Try it:**

* Use `:vimgrep` to find `target` in this file, open the quickfix window, and jump through results.

```
# target appearances
- no target here
- target acquired
- retarget and target again
```

---

## 17) Terminal and external commands (Neovim)

**Goal:** Use Nvim extras.

**Know:**

* Open terminal: `:terminal`
* Leave Terminal‑job to Normal: `<C-\><C-n>`
* Filter through external command: visual select then `:!sort`
* Read command output: `:read !date`

**Try it:**

* Visual select the block below and run `:!sort` to sort the lines.

```
delta
alpha
gamma
beta
```

---

## 18) Help like a pro

**Goal:** Find answers fast.

**Know:**

* `:help quickref` overview
* `:help {topic}` exact, `K` for manpage of word under cursor
* Jump inside help: `<C-]>` follow tag, `<C-t>` back
* Search all help: `:helpgrep pattern` then `:copen`

**Try it:**

* Run `:help text-objects` then follow a `iw` tag with `<C-]>` and jump back.

---

## 19) Leader practice (`,`)

**Goal:** Practice using a leader.

**Note:** This file does not define mappings. Pretend you mapped the following in your config:

```
nnoremap ,s :%s///g<Left><Left>
nnoremap ,w :w<CR>
nnoremap ,q :q<CR>
```

**Try it:**

* Place cursor on a word and trigger `,s` to prefill a substitute. Finish it.
* Use `,w` then `,q` to simulate save and quit.

---

## 20) Mini‑workout: from raw text to clean list

**Goal:** Combine motions, operators, macros, substitute.

**Task:** Turn the messy lines into `- Key: Value` format, sorted, duplicates removed.

1. Record a macro in `qa` that transforms one line.
2. Apply with a count to the block.
3. Use `:%s/\v\s+/ /g` to normalize spaces.
4. Sort unique with `:%!sort -u` (requires external sort).

```
Value=  99   ; Key= speed
Key= Name ; Value=  Alice
Value =  42 ;  Key = answer
Key=Name ; Value=Alice
```

---

## Appendix A: 100 core commands checklist

Mark each when you feel confident.

**Movement:** `h` `j` `k` `l` `w` `W` `b` `B` `e` `E` `ge` `gE` `0` `^` `$` `g_` `gg` `G` `H` `M` `L` `%` `(` `)` `{` `}` `zt` `zz` `zb` `ctrl-d` `ctrl-u`

**Find/Till:** `f` `F` `t` `T` `;` `,`

**Insert/Replace:** `i` `I` `a` `A` `o` `O` `r` `R` `s` `S`

**Operators:** `d{motion}` `c{motion}` `y{motion}` `gU{motion}` `gu{motion}` `~` `>` `<` `J` `gJ`

**Linewise:** `dd` `cc` `yy` `D` `C` `Y` `p` `P` `gp` `gP`

**Visual:** `v` `V` `<C-v>` `o` `gv` `aw` `iw` `aW` `iW` `a)` `i)` `a]` `i]` `a}` `i}` `a"` `i"` `ap` `ip`

**Search:** `/` `?` `n` `N` `*` `#` `g*` `g#` `:noh`

**Substitute:** `:s` `:%s` `\v` `\<` `\>`

**Windows/Tabs:** `:split` `:vsplit` `<C-w>h` `<C-w>j` `<C-w>k` `<C-w>l` `<C-w>w` `<C-w>=` `<C-w>_` `<C-w>|` `<C-w>q` `<C-w>o` `:tabnew` `gt` `gT` `:tabclose`

**Buffers/Files:** `:e` `:w` `:q` `:x` `ZZ` `ZQ` `:wq` `:q!` `:bd` `:ls` `:bn` `:bp` `<C-^>` `:saveas` `:r` `:read !{cmd}`

**Marks/Jumps:** `ma` `` `a `` `'a` `<C-o>` `<C-i>` `` `. `` `` `" ``

**Registers:** `:reg` `"a` `"+` `"*` `"_` `"ayy` `"ap`

**Macros:** `qa` `q` `@a` `@@` `:normal` with range

**Formatting/Indent:** `=` `gg=G` `={motion}` `>>` `<<` `gq` `:set textwidth`

**Folding:** `zf` `zd` `za` `zc` `zo` `zM` `zR` `:set foldmethod=`

**Quickfix/Grep:** `:vimgrep` `:copen` `:cnext` `:cprev` `:clist` `:cclose`

**Help:** `:help` `:helpgrep` `<C-]>` `<C-t>` `K`

**Neovim:** `:terminal` `<C-\><C-n>` `:checkhealth` `:Tutor`

---

## Appendix B: Daily 5‑minute drills

1. Open any file. Spend one minute moving with only `w/b/e/ge` and counts.
2. Spend one minute doing `d`/`c` + motions only. No Visual.
3. Spend one minute practicing `f`/`t` with `;` and `,`.
4. Spend one minute of `*`/`#` then `:%s` with `c` confirm.
5. Spend one minute recording and playing a macro across lines.

---

You are done when you can complete every section without thinking. If you hesitate, run `:help` on that topic and try again.
