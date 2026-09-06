const testDataEl = document.getElementById('test-data');
const deadlineISO = testDataEl.dataset.deadline;
const questionLangs = JSON.parse("{" + testDataEl.dataset.langs + "}");

const editors = {};

require.config({ paths: { vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs' } });

require(['vs/editor/editor.main'], function () {
    Object.keys(questionLangs).forEach(function (qid) {
        let lang = questionLangs[qid];
        let monacoLang = { c: 'c', cpp: 'cpp', java: 'java', python: 'python', sql: 'sql' }[lang] || 'plaintext';

        editors[qid] = monaco.editor.create(document.getElementById('editor-' + qid), {
            value: document.getElementById('code_' + qid).value || '',
            language: monacoLang,
            theme: 'vs-dark',
            fontSize: 14,
            automaticLayout: true,
            minimap: { enabled: false }
        });
    });
});

function syncAllEditorsToTextareas() {
    Object.keys(editors).forEach(function (qid) {
        document.getElementById('code_' + qid).value = editors[qid].getValue();
    });
}