import { useMemo, useRef, useState } from 'react';
import { ChevronDown, ChevronsDownUp, ChevronsUpDown } from 'lucide-react';

function splitLessonContent(html) {
  if (!html || typeof window === 'undefined') return null;

  const doc = new DOMParser().parseFromString(html, 'text/html');
  const nodes = Array.from(doc.body.childNodes);
  const nodeHtml = (node) => (node.nodeType === 1 ? node.outerHTML : node.textContent || '');

  // Lessons are seeded with either <h2> or <h3> as the top-level section
  // heading depending on whether the lesson title itself is wrapped in an
  // <h2> — pick whichever tag actually repeats.
  const h2Count = nodes.filter((n) => n.nodeType === 1 && n.tagName === 'H2').length;
  const headingTag = h2Count > 1 ? 'H2' : 'H3';

  const introParts = [];
  const rawSections = [];
  let current = null;

  for (const node of nodes) {
    if (node.nodeType === 1 && node.tagName === headingTag) {
      current = { title: node.textContent, parts: [] };
      rawSections.push(current);
    } else if (current) {
      current.parts.push(nodeHtml(node));
    } else {
      introParts.push(nodeHtml(node));
    }
  }

  if (rawSections.length < 2) return null;

  return {
    introHtml: introParts.join(''),
    sections: rawSections.map((s) => ({ title: s.title, html: s.parts.join('') })),
  };
}

export default function LessonContentAccordion({ content }) {
  const parsed = useMemo(() => splitLessonContent(content), [content]);
  const [openIndexes, setOpenIndexes] = useState(() => new Set([0]));
  const sectionRefs = useRef([]);

  if (!parsed) {
    return (
      <div className="prose prose-lg max-w-none dark:prose-invert">
        <div dangerouslySetInnerHTML={{ __html: content }} />
      </div>
    );
  }

  const { introHtml, sections } = parsed;

  const toggle = (i) => {
    setOpenIndexes((prev) => {
      const next = new Set(prev);
      if (next.has(i)) next.delete(i);
      else next.add(i);
      return next;
    });
  };

  const expandAll = () => setOpenIndexes(new Set(sections.map((_, i) => i)));
  const collapseAll = () => setOpenIndexes(new Set());

  const jumpTo = (i) => {
    setOpenIndexes((prev) => new Set(prev).add(i));
    requestAnimationFrame(() => {
      sectionRefs.current[i]?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  };

  return (
    <div className="lg:flex lg:gap-8 lg:items-start">
      <div className="hidden lg:block lg:w-56 lg:shrink-0 lg:sticky lg:top-24 lg:self-start">
        <p className="text-xs font-semibold uppercase tracking-wide text-gray-400 dark:text-gray-500 mb-2">
          On this page
        </p>
        <nav className="space-y-1 border-l border-gray-200 dark:border-gray-700">
          {sections.map((s, i) => (
            <button
              key={i}
              onClick={() => jumpTo(i)}
              className={`block w-full text-left text-sm pl-3 py-1 border-l-2 -ml-px transition-colors ${
                openIndexes.has(i)
                  ? 'border-primary-600 text-primary-600 dark:text-primary-400 font-medium'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'
              }`}
            >
              {s.title}
            </button>
          ))}
        </nav>
      </div>

      <div className="min-w-0 flex-1">
        {introHtml && (
          <div
            className="prose prose-lg max-w-none dark:prose-invert mb-4"
            dangerouslySetInnerHTML={{ __html: introHtml }}
          />
        )}

        <div className="flex justify-end gap-4 mb-2 text-sm">
          <button
            onClick={expandAll}
            className="flex items-center gap-1 text-primary-600 hover:text-primary-500 dark:text-primary-400 font-medium"
          >
            <ChevronsUpDown size={14} /> Expand all
          </button>
          <button
            onClick={collapseAll}
            className="flex items-center gap-1 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 font-medium"
          >
            <ChevronsDownUp size={14} /> Collapse all
          </button>
        </div>

        <div className="divide-y divide-gray-200 dark:divide-gray-700 border-y border-gray-200 dark:border-gray-700">
          {sections.map((s, i) => {
            const isOpen = openIndexes.has(i);
            return (
              <div key={i} ref={(el) => (sectionRefs.current[i] = el)}>
                <button
                  onClick={() => toggle(i)}
                  className="w-full flex items-center justify-between gap-4 py-4 text-left"
                  aria-expanded={isOpen}
                >
                  <span className="text-lg font-semibold text-gray-900 dark:text-white">{s.title}</span>
                  <ChevronDown
                    size={20}
                    className={`shrink-0 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`}
                  />
                </button>
                {isOpen && (
                  <div
                    className="prose prose-lg max-w-none dark:prose-invert pb-6"
                    dangerouslySetInnerHTML={{ __html: s.html }}
                  />
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
