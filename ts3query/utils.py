unescaped = ["\\", "/", " ", "|", "\a", "\b", "\f", "\n", "\r", "\t", "\v"]
escaped = ["\\\\", "\\/", "\\s", "\\p", "\\a", "\\b", "\\f", "\\n", "\\r", "\\t", "\\v"]

def translate(text, i, o):
    if len(i) != len(o):
        raise ValueError("Translation table incorrect (different lengths)")
    for x in range(len(i)):
        text = text.replace(i[x], o[x])
    return text

def escape(text):
    return translate(text, unescaped, escaped)

def unescape(text):
    return translate(text, escaped, unescaped)
