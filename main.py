from session import Session

def main():
    session = Session()
    session.cmdloop(session.welcome_str)
    
if __name__=="__main__": 
    main()