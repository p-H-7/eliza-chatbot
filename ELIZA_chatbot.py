import re
import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class Eliza:
    def __init__(self):
        self.patterns = [
            # I am patterns
            (r'.*i am (.*)', [
                "Why are you {0}?",
                "How long have you been {0}?",
                "Do you believe it's normal to be {0}?",
                "Do you enjoy being {0}?"
            ]),
            
            # I feel patterns
            (r'.*i feel (.*)', [
                "Why do you feel {0}?",
                "Do you often feel {0}?",
                "When do you usually feel {0}?",
                "What makes you feel {0}?"
            ]),
            
            # Family patterns
            (r'.*mother.*', [
                "Tell me more about your mother.",
                "What was your relationship with your mother like?",
                "How do you feel about your mother?",
                "Does your mother influence you much?"
            ]),
            
            (r'.*father.*', [
                "Tell me more about your father.",
                "How did your father make you feel?",
                "What role does your father play in your life?",
                "Do you have a good relationship with your father?"
            ]),
            
            # I want/need patterns
            (r'.*i want (.*)', [
                "What would it mean to you if you got {0}?",
                "Why do you want {0}?",
                "What would you do if you got {0}?",
                "Suppose you got {0} soon. What then?"
            ]),
            
            (r'.*i need (.*)', [
                "Why do you need {0}?",
                "Would it really help you to get {0}?",
                "Are you sure you need {0}?",
                "What would getting {0} mean to you?"
            ]),
            
            # Questions about ELIZA
            (r'.*you.*', [
                "We're here to talk about you, not me.",
                "Why do you ask about me?",
                "What does it matter whether I {0}?",
                "Let's focus on your feelings instead."
            ]),
            
            # Yes/No responses
            (r'^yes$', [
                "You seem quite sure.",
                "OK, but can you elaborate a bit?",
                "I understand. Can you tell me more?",
                "Why do you think so?"
            ]),
            
            (r'^no$', [
                "Why not?",
                "OK, but can you elaborate a bit?",
                "Are you saying no just to be negative?",
                "You seem very certain. Why?",
                "You sure do like saying no. Why?"
            ]),
            
            # Dreams
            (r'.*i had a dream (.*)', [
                "Dreams can be very meaningful. What do you think this dream means?",
                "What do you think the dream was about?",
                "How did the dream make you feel?",
                "Do you often have dreams like this?"
            ]),

            # I think/believe patterns
            (r'.*i think (.*)', [
                "Do you doubt {0}?",
                "Do you really think so?",
                "But you're not sure {0}?",
                "What makes you think {0}?"
            ]),
            
            (r'.*i believe (.*)', [
                "Do you really believe {0}?",
                "But you're not certain {0}?",
                "What makes you believe {0}?",
                "Do you have doubts about {0}?"
            ]),
            
            # I can't/don't patterns
            (r'.*i can\'?t (.*)', [
                "How do you know you can't {0}?",
                "Perhaps you could {0} if you tried.",
                "What would it take for you to {0}?",
                "Have you really tried to {0}?"
            ]),
            
            (r'.*i don\'?t (.*)', [
                "Don't you really {0}?",
                "Why don't you {0}?",
                "Do you want to {0}?",
                "What would make you {0}?"
            ]),
            
            # I have/had patterns
            (r'.*i have (.*)', [
                "How long have you had {0}?",
                "What does having {0} mean to you?",
                "How do you feel about having {0}?",
                "What would it be like if you didn't have {0}?"
            ]),
            
            (r'.*i had (.*)', [
                "How did having {0} make you feel?",
                "What was it like when you had {0}?",
                "How do you feel about losing {0}?",
                "Do you miss having {0}?"
            ]),
            
            # I love/hate patterns
            (r'.*i love (.*)', [
                "What do you love most about {0}?",
                "Why do you love {0}?",
                "How does {0} make you feel?",
                "What would happen if you lost {0}?"
            ]),
            
            (r'.*i hate (.*)', [
                "What do you hate most about {0}?",
                "Why do you hate {0}?",
                "What would it take for you to not hate {0}?",
                "How long have you hated {0}?"
            ]),
            
            # I'm afraid/scared patterns
            (r'.*i\'?m afraid (.*)', [
                "What frightens you most about {0}?",
                "How long have you been afraid of {0}?",
                "Do you think your fear of {0} is reasonable?",
                "What would help you overcome your fear of {0}?"
            ]),
            
            (r'.*i\'?m scared (.*)', [
                "What scares you most about {0}?",
                "When did you first become scared of {0}?",
                "How does being scared of {0} affect your life?",
                "What would make you feel less scared of {0}?"
            ]),
            
            # Everyone/nobody patterns
            (r'.*everyone (.*)', [
                "Really, everyone?",
                "Surely not everyone {0}.",
                "Can you think of anyone who doesn't {0}?",
                "Who in particular are you thinking of?"
            ]),
            
            (r'.*nobody (.*)', [
                "Really, nobody?",
                "Surely someone {0}.",
                "Can you think of anyone who does {0}?",
                "What makes you think nobody {0}?"
            ]),
            
            # Always/never patterns
            (r'.*always (.*)', [
                "Really, always?",
                "Can you think of a time when that wasn't true?",
                "What do you think makes it always {0}?",
                "Are you sure it's always {0}?"
            ]),
            
            (r'.*never (.*)', [
                "Never?",
                "Can you think of a time when you did {0}?",
                "What would it take for you to {0}?",
                "How do you feel about never {0}?"
            ]),
            
            # Work/job patterns
            (r'.*my work.*', [
                "Tell me more about your work.",
                "How do you feel about your work?",
                "What do you like most about your work?",
                "What would you change about your work?"
            ]),
            
            (r'.*my job.*', [
                "What do you like about your job?",
                "How does your job make you feel?",
                "Do you find your job fulfilling?",
                "What would your ideal job be like?"
            ]),
            
            # Relationship patterns
            (r'.*my (wife|husband|partner|boyfriend|girlfriend) (.*)', [
                "How do you feel about your {0}?",
                "What is your relationship with your {0} like?",
                "How long have you been with your {0}?",
                "What do you value most about your {0}?"
            ]),
            
            (r'.*my friend.*', [
                "Tell me more about your friend.",
                "What do you value in friendship?",
                "How do your friends make you feel?",
                "What kind of friend are you?"
            ]),
            
            # Problems/issues patterns
            (r'.*my problem.*', [
                "What makes this a problem for you?",
                "How long has this been a problem?",
                "What would solving this problem mean to you?",
                "Have you tried to solve this problem before?"
            ]),
            
            (r'.*i\'?m having trouble (.*)', [
                "What kind of trouble are you having with {0}?",
                "How long have you been having trouble with {0}?",
                "What do you think is causing the trouble with {0}?",
                "What would help you with {0}?"
            ]),
            
            # Greeting patterns
            (r'^(hi|hello|hey)$', [
                "Hello! How are you feeling today?",
                "Hi there! What's on your mind?",
                "Hello! What would you like to talk about?",
                "Hi! How can I help you today?"
            ]),

            # Default responses when no pattern matches
            (r'.*', [
                "Please tell me more.",
                "Let's change focus a bit... Tell me about your family.",
                "Can you elaborate on that?",
                "Why do you say that?",
                "I see.",
                "Very interesting.",
                "I see. And what does that tell you?",
                "How does that make you feel?",
                "How do you feel when you say that?"
            ])
        ]
    
    def respond(self, text):
        # Convert to lowercase for matching
        text = text.lower().strip()
        
        # Check each pattern
        for pattern, responses in self.patterns:
            match = re.search(pattern, text)
            if match:
                # Pick a random response from the list
                response = random.choice(responses)
                # If the response has placeholders AND we have captured groups, fill them
                if '{0}' in response and match.groups() and match.group(1):
                    # Transform pronouns
                    matched_text = self.transform_pronouns(match.group(1))
                    response = response.format(matched_text)
                elif '{0}' in response:
                    # If there's a {0} but no captured group, remove the placeholder
                    response = response.replace(' {0}', '').replace('{0}', '')
                return response
        
        # This shouldn't happen since we have a catch-all pattern
        return "Please tell me more."
    
    def transform_pronouns(self, text):
        """Transform pronouns from user's perspective to therapist's perspective"""
        transformations = {
            'i': 'you',
            'me': 'you', 
            'my': 'your',
            'mine': 'yours',
            'you': 'I',
            'your': 'my',
            'yours': 'mine'
        }
        
        words = text.split()
        transformed_words = []
        
        for word in words:
            # Handle punctuation
            clean_word = word.strip('.,!?;:')
            punctuation = word[len(clean_word):]
            
            if clean_word.lower() in transformations:
                transformed_words.append(transformations[clean_word.lower()] + punctuation)
            else:
                transformed_words.append(word)
        
        return ' '.join(transformed_words)

# def main():
#     eliza = Eliza()
    
#     print("ELIZA: Hello! I'm ELIZA. How are you feeling today?")
#     print("(Type 'quit' to exit)")
    
#     while True:
#         user_input = input("You: ")
        
#         if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
#             print("ELIZA: Goodbye! It was nice talking with you.")
#             break
        
#         response = eliza.respond(user_input)
#         print(f"ELIZA: {response}")

eliza = Eliza()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    eliza_response = eliza.respond(user_message)
    return jsonify({'response': eliza_response})

if __name__ == '__main__':
    app.run(debug=True)