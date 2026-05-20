try:
    from presidio_analyzer import AnalyzerEngine
    from presidio_anonymizer import AnonymizerEngine

    _analyzer = AnalyzerEngine()
    _anonymizer = AnonymizerEngine()
    _PRESIDIO_AVAILABLE = True
except ImportError:
    _PRESIDIO_AVAILABLE = False


def mask(text: str) -> str:
    if not _PRESIDIO_AVAILABLE or not text:
        return text
    results = _analyzer.analyze(text=text, language="en")
    if not results:
        return text
    return _anonymizer.anonymize(text=text, analyzer_results=results).text
