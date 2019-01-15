
def article_read_time(article):
    """
    calculates the average reading time of an article
    based on average reading speed of an adult
    (265WPM)

    Args:
        article(String): article to estimate

    returns:
        (String): estimate read time
    """
    word_count = len(article.split(' '))
    seconds = int(((word_count*60)/265))

    if seconds < 60:
        return "less than 1 min"

    elif seconds < 3600:
        time = int((seconds/60))
        return str(time)+ " mins"

    elif seconds < 24*3600:
        hrs = int((seconds/3600))
        mins = int((seconds%3600)/60)
        return str(hrs)+" hrs and "+str(mins)+" mins"

    else:
        return "more than 1 day"

