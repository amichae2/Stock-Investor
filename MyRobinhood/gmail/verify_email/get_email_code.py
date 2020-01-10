from MyRobinhood.gmail.verify_email import get_email, create_gmail_service, list_email


def get_email_code(user_id, includeSpamTrash, maxResults, query):
    """gets email code sent to gmail by challnge from Robinhood"""

    service = create_gmail_service.create_service()

    #get list of robinhood emails
    messages = list_email.ListMessagesMatchingQuery(service=service, user_id=user_id,
                                                    include_spam_trash=includeSpamTrash, max_results=maxResults,
                                                    query=query)

    # get message id
    message_id = str([sub['id'] for sub in messages])

    # use message id to get email with corresponding message id
    if message_id != None:
        email = get_email.GetMimeMessage(service=service, user_id=user_id, msg_id=message_id)

    # search email for code
    values = email.values()
    print(values)


    # get code
    # send code to robinhood
