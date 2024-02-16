from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST

def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses

def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to Django session.
    '''
    if answer:
        # Retrieve the list of valid answers for the current question
        valid_answers = [question['valid_answers'] for question in PYTHON_QUESTION_LIST if question['id'] == current_question_id]
        
        # Check if the user's answer matches any of the valid answers
        if any(answer.lower() in map(str.lower, valid_answers)):
            session[f"answer_{current_question_id}"] = answer
            session.save()
            return True, ""
        else:
            return False, "Error: Invalid answer. Please provide a valid answer."
    else:
        return False, "Error: No answer provided."

def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current question ID.
    '''
    for i, question_info in enumerate(PYTHON_QUESTION_LIST):
        if question_info['id'] == current_question_id:
            if i + 1 < len(PYTHON_QUESTION_LIST):
                next_question = PYTHON_QUESTION_LIST[i + 1]['question']
                next_question_id = PYTHON_QUESTION_LIST[i + 1]['id']
                return next_question, next_question_id
    return None, None

def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    total_score = 0
    total_questions = len(PYTHON_QUESTION_LIST)
    for question_info in PYTHON_QUESTION_LIST:
        question_id = question_info['id']
        user_answer = session.get(f"answer_{question_id}")
        if user_answer:
            # Here you can implement scoring logic based on user answers
            # For simplicity, let's assume each correct answer adds 1 to the score
            if user_answer == question_info['correct_answer']:
                total_score += 1

    # You can customize the final result message based on the score or any other criteria
    final_result_message = f"Thank you for answering {total_score}/{total_questions} questions correctly!"
    return final_result_message
