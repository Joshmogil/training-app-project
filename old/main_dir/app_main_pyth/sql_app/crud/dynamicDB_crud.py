
from sqlalchemy import select
from sqlalchemy.orm import Session
from sql_app.crud.models import goalsListSplitsList
from ..database import engine, goals, splits, user_misc


def get_all_goals_and_all_splits(db: Session):
    
    goalsAndSplits = {}

    goalsList = []
    splitsList =[]


    s = select(goals)

    for row in db.execute(s):       
        row = dict(row)
              
        goalsList.append(row["name"]) 

    s = select(splits)
    for row in db.execute(s):        
        row = dict(row)
                
        splitsList.append(row["name"]) 

    goalsAndSplits["goals"] = goalsList
    goalsAndSplits["splits"]= splitsList

    return goalsAndSplits