"""Diagrams, labs, references and glossary.

The registries are populated by import side effects (``@register`` plus lazy
``pkgutil`` loading), so a module file that fails to import silently loses every
diagram in it. These tests force the load and check the wiring both ways: nothing a
lecture embeds is missing, and nothing registered is stranded.
"""

import re

import pytest

import components.diagrams as diagrams
import components.labs as labs

DIAGRAM_TOKEN = re.compile(r"\[\[diagram:([a-z0-9_]+)\]\]")
WIDGET_TOKEN = re.compile(r"\[\[widget:([a-z0-9_]+)\]\]")

# Registered for the standalone pages rather than embedded in a lecture body.
PAGE_LEVEL_DIAGRAMS = {"course_map", "knowledge_map", "learning_journey"}


@pytest.fixture(scope="session")
def registered_diagrams():
    return set(diagrams.names())


@pytest.fixture(scope="session")
def registered_labs():
    return {lab.name: lab for lab in labs.all_labs()}


@pytest.fixture(scope="session")
def embedded(lectures, modules):
    """Every diagram and widget name the content actually asks for."""
    d, w = set(), set()
    for lec in lectures:
        d |= set(DIAGRAM_TOKEN.findall(lec.body))
        w |= set(WIDGET_TOKEN.findall(lec.body))
    for m in modules:
        if m.meta.get("concept_diagram"):
            d.add(m.meta["concept_diagram"])
    return d, w


def test_registries_are_not_empty(registered_diagrams, registered_labs):
    """A broken import in one module file would show up here as a big drop."""
    assert len(registered_diagrams) >= 100, f"only {len(registered_diagrams)} diagrams loaded"
    assert len(registered_labs) >= 35, f"only {len(registered_labs)} labs loaded"


def test_every_embedded_diagram_is_registered(embedded, registered_diagrams):
    used, _ = embedded
    missing = sorted(used - registered_diagrams)
    assert not missing, f"lectures embed unregistered diagrams: {missing}"


def test_every_embedded_widget_is_registered(embedded, registered_labs):
    _, used = embedded
    missing = sorted(used - set(registered_labs))
    assert not missing, f"lectures embed unregistered labs: {missing}"


def test_no_orphan_diagrams(embedded, registered_diagrams):
    """A registered diagram nobody embeds is dead weight the reader never sees."""
    used, _ = embedded
    orphans = sorted(registered_diagrams - used - PAGE_LEVEL_DIAGRAMS)
    assert not orphans, f"registered but never embedded: {orphans}"


def test_no_orphan_labs(embedded, registered_labs):
    _, used = embedded
    orphans = sorted(set(registered_labs) - used)
    assert not orphans, f"registered but never embedded: {orphans}"


def test_every_module_has_a_concept_diagram(modules, registered_diagrams):
    for m in modules:
        name = m.meta.get("concept_diagram")
        assert name, f"module {m.number}: no concept_diagram"
        assert name in registered_diagrams, f"module {m.number}: unknown diagram {name!r}"


def test_labs_declare_their_module(registered_labs, modules):
    numbers = {m.number for m in modules}
    for name, lab in registered_labs.items():
        assert lab.module in numbers, f"lab {name}: module {lab.module} does not exist"
        assert lab.title, f"lab {name}: no Arabic title"
        assert lab.title_en, f"lab {name}: no English title"


def test_lab_widget_keys_are_namespaced(registered_labs):
    """Two labs on one page must not collide on a Streamlit key, so every key a lab
    creates is prefixed with the lab's own name."""
    import inspect

    offenders = []
    for name, lab in registered_labs.items():
        module_prefix = name.split("_")[0]  # e.g. "m10"
        for key in re.findall(r'key=f?"([^"{]+)', inspect.getsource(lab.fn)):
            if not key.startswith(module_prefix):
                offenders.append(f"{name}: key {key!r} does not start with {module_prefix!r}")
    assert not offenders, "labs with un-namespaced widget keys:\n  " + "\n  ".join(offenders)


def test_references_are_complete(references):
    for rid, ref in references.items():
        for field in ("id", "authors", "year", "title", "type", "topic"):
            assert ref.get(field), f"reference {rid}: missing {field!r}"
        assert ref.get("url") or ref.get("doi"), f"reference {rid}: needs a url or a doi"
        assert ref.get("verified"), f"reference {rid}: no verification date"


def test_reference_ids_match_their_keys(references):
    for rid, ref in references.items():
        assert ref["id"] == rid, f"reference keyed {rid!r} declares id {ref['id']!r}"


def test_no_orphan_references(references, lectures, modules):
    """Every source in references.yml is actually reachable by a reader: cited in a
    lecture's front matter, listed as suggested reading, or linked as a self-study item."""
    cited = set()
    self_study_urls = set()
    for lec in lectures:
        for item in lec.meta.get("references") or []:
            cited.add(item["id"] if isinstance(item, dict) else item)
        for item in lec.meta.get("self_study") or []:
            self_study_urls.add(str(item.get("url", "")).rstrip("/"))
    for m in modules:
        cited |= set(m.meta.get("exit", {}).get("suggested_reading", []))

    orphans = []
    for rid, ref in references.items():
        if rid in cited:
            continue
        links = {str(ref.get("url", "")).rstrip("/")}
        if ref.get("doi"):
            links.add(f"https://doi.org/{ref['doi']}")
        if not (links & self_study_urls):
            orphans.append(rid)
    assert not orphans, f"references defined but never cited or linked: {sorted(orphans)}"


def test_glossary_entries_are_complete(glossary, modules):
    numbers = {m.number for m in modules}
    for term in glossary:
        for field in ("ar", "en", "definition", "module"):
            assert term.get(field), f"glossary {term.get('en') or term.get('ar')}: missing {field!r}"
        assert term["module"] in numbers, \
            f"glossary {term['en']}: module {term['module']} does not exist"


def test_glossary_english_terms_are_unique(glossary):
    seen = {}
    for term in glossary:
        key = term["en"].strip().lower()
        assert key not in seen, (
            f"glossary term {term['en']!r} defined twice "
            f"(modules {seen.get(key)} and {term['module']})"
        )
        seen[key] = term["module"]


def test_glossary_lecture_links_resolve(glossary, lectures):
    known = {lec.id for lec in lectures}
    for term in glossary:
        if term.get("lecture"):
            assert term["lecture"] in known, \
                f"glossary {term['en']}: unknown lecture {term['lecture']!r}"
