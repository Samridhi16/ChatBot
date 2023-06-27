import requests
import nltk

def extract_named_entities(message):
    # Download required NLTK resources
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')

    # Tokenize the user's message into sentences
    sentences = nltk.sent_tokenize(message)

    # Extract named entities from each sentence
    named_entities = []
    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)
        entities = nltk.ne_chunk(tagged)
        for entity in entities:
            if hasattr(entity, 'label') and entity.label:
                named_entities.append((entity.label(), ' '.join(child[0] for child in entity.leaves())))

    return named_entities


def generate_response(message):
    named_entities = extract_named_entities(message)
    for entity in named_entities:
        if entity[0] == 'PERSON':
            person_name = entity[1]
            return f"Hello! {person_name}"

    # If no named entities found or no specific response generated
    return "Hello! How can I assist you today?"

if __name__ == '__main__':
    print(generate_response("Hi, I am George"))