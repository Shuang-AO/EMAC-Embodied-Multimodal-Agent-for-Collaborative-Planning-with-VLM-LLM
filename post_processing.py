import re
import string

def process_ob(ob):
    if ob.startswith('You arrive at loc '):
        ob = ob[ob.find('. ')+2:]    
    return ob

def remove_the(sentence):
    if 'the' in sentence:
        words = sentence.split(' ')
        words = [word for word in words if word.lower() != 'the']
        sentence = ' '.join(words)

    sentence = ' '.join(sentence.split())

    return sentence.strip()

def check_put(action):
    action = remove_the(action)

    pattern1 = r'put (.*) in (.*)'  
    pattern2 = r'put (.*) on (.*)'  

    match = re.match(pattern1, action)
    if match:
        return f"put {match.group(1)} in/on {match.group(2)}"

    match = re.match(pattern2, action)
    if match:
        return f"put {match.group(1)} in/on {match.group(2)}"

    return action

def check_goto(action):
    action = remove_the(action)
    words = action.split(" ")
    return " ".join(words[:4])

def check_use(action):
    action = remove_the(action)
    words = action.split(" ")
    return " ".join(words[:3])

def action_postprocess(action):
    action = action.strip(string.punctuation)
    action = str(action).lower().strip()

    if action.startswith('>'):
        action = action.split(">")[1].strip()

    if action.startswith('put'):
        return check_put(action)
    
    if action.startswith('go'):
        return check_goto(action)
    
    if action.startswith('use'):
        return check_use(action)
    elif action.startswith('open'):
        return check_use(action)
    elif action.startswith('open'):
        return check_use(action)
    elif action.startswith('examine'):
        return check_use(action)
    elif action.startswith('close'):
        return check_use(action)
    
    if action.startswith('heat'):
        return remove_the(action)
    elif action.startswith('cool'):
        return remove_the(action)
    elif action.startswith('clean'):
        return remove_the(action)
    elif action.startswith('take'):
        return remove_the(action)
    
    return action


if __name__ == "__main__":
    examples = [
        'go to the cabinet 1',
        'take the coffee cup 1 from the table 1',
        'examine the cabinet 1',
        'close the fridge 1',
        'use the fridge 1',
        'open the fridge 1',
        'put the apple 1 in the fridge 1',
        'put the apple 1 on the fridge 1',
        'heat the apple 1 with the microwave 1',
        'cool the apple 1 with the microwave 1',
        'clean the apple 3 with the sinkbasin 1',
        'clean the apple 3 with the sinkbasin 1 (ok (ok'
    ]
    for example in examples:
        print(action_postprocess(example))