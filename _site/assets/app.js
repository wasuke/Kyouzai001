"use strict";
(() => {
  const $ = id => document.getElementById(id);
  const lesson = $("lesson"), material = $("material"), copy = $("copy");
  const code = $("code"), status = $("status"), manual = $("select-code");
  const data = window.CODE_LIBRARY;
  let current = null, revision = 0;
  function showCode() {
    revision++;
    current = data.lessons[Number(lesson.value)].codes[Number(material.value)] || null;
    code.textContent = current ? current.content : "この回の教材は準備中です。";
    $("code-title").textContent = current ? current.name : "教材は準備中です";
    $("lesson-label").textContent = data.lessons[Number(lesson.value)].title;
    $("filename").textContent = current ? current.filename : "未登録";
    const count = current ? (current.content ? current.content.replace(/\r?\n$/, "").split("\n").length : 0) : 0;
    $("lines").textContent = current ? `${count} 行` : "";
    copy.disabled = !current; copy.textContent = "コードをコピー";
    manual.hidden = true;
    status.textContent = current ? "コードをコピーして、指定のエディタに貼り付けましょう。" : "先生の案内をお待ちください。";
    $("code-panel").scrollTop = 0; $("code-panel").scrollLeft = 0;
  }
  function showLesson() {
    const codes = data.lessons[Number(lesson.value)].codes;
    material.replaceChildren();
    codes.forEach((entry, i) => material.add(new Option(entry.name, String(i))));
    if (!codes.length) material.add(new Option("教材は準備中です", ""));
    material.disabled = !codes.length;
    $("count").textContent = `${codes.length} 件の教材`;
    showCode();
  }
  manual.addEventListener("click", () => {
    const range = document.createRange(); range.selectNodeContents(code);
    const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range);
    status.textContent = "コードを選択しました。Ctrl+C（Macは⌘C）、または選択範囲のメニューでコピーしてください。";
  });
  copy.addEventListener("click", async () => {
    if (!current) return;
    const version = revision, content = current.content;
    copy.disabled = true;
    try {
      await navigator.clipboard.writeText(content);
      if (version !== revision) return;
      status.textContent = "コピーしました！ 指定のエディタに貼り付けてください。";
      copy.textContent = "✓ コピーしました";
    } catch {
      if (version !== revision) return;
      status.textContent = "自動コピーが使えません。下のボタンでコードを選択し、手動でコピーしてください。";
      manual.hidden = false;
    } finally { if (version === revision) copy.disabled = false; }
  });
  if (!data || !Array.isArray(data.lessons) || data.lessons.length !== 6) {
    status.textContent = "教材を読み込めませんでした。ページを再読み込みしてください。解消しない場合は先生にお知らせください。";
    lesson.replaceChildren(new Option("読み込みエラー", ""));
    return;
  }
  lesson.replaceChildren();
  data.lessons.forEach((entry, i) => lesson.add(new Option(entry.title, String(i))));
  lesson.disabled = false;
  lesson.addEventListener("change", showLesson); material.addEventListener("change", showCode);
  showLesson();
})();
