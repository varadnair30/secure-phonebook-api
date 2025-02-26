
# Import the required modules
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import re

# Create the FastAPI app
app = FastAPI()

# Create the SQLite database engine for PhoneBook
phonebook_engine = create_engine("sqlite:///phonebook.db", echo=True)
# Create the base class for the database models for PhoneBook
PhoneBookBase = declarative_base()

# Create the SQLite database engine for AuditLog
auditlog_engine = create_engine("sqlite:///auditlog.db", echo=True)
# Create the base class for the database models for AuditLog
AuditLogBase = declarative_base()

# Create the PhoneBook model class
class PhoneBook(PhoneBookBase):
    __tablename__ = "phonebook"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    phone_number = Column(String)

# Create the AuditLog model class
class AuditLog(AuditLogBase):
    __tablename__ = "auditlog"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True)
    event_data = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create the database schema for PhoneBook
PhoneBookBase.metadata.create_all(phonebook_engine)
# Create the database schema for AuditLog
AuditLogBase.metadata.create_all(auditlog_engine)

# Create the session class for PhoneBook database operations
PhoneBookSession = sessionmaker(bind=phonebook_engine)
# Create the session class for AuditLog database operations
AuditLogSession = sessionmaker(bind=auditlog_engine)

def name_check(name):
    if not re.match("^[a-zA-Z(')?\-]+(,)?(\s)?([a-zA-Z\-]+(')?[a-zA-Z\-]+)?(\s)?([a-zA-Z'\-]+)?(.)?$", name):
        return False
    if  re.match(".*''.*", name):
        return False
    if  re.match(".*\-.*\-.*", name):
        return False

    return True
def phone_check(phone_number):
    ''' check number is in this format: #####'''
    if  re.match("^\d{5}$", phone_number):
        return True

    ''' check number is in this format: ###-###-####'''
    if  re.match("^\d{3}-\d{3}-\d{4}$", phone_number):
        return True

    ''' check number is in this format: (###) ###-####'''
    if  re.match("^\(\d{3}\)\s\d{3}-\d{4}$", phone_number):
        return True

    ''' check number is in this format: (###)###-####'''
    if  re.match("^\(\d{3}\)\d{3}-\d{4}$", phone_number):
        return True

    ''' check number is in this format: ### ### ####'''
    if  re.match("^\d{3}\s\d{3}\s\d{4}$", phone_number):
        return True

    '''check number if is in this format:#####.#####'''
    if  re.match("^\d{5}\.\d{5}$", phone_number):
        return True

    '''check number if is this format: ### # ### ### ####'''
    if  re.match("^\d{3}\s\d{1}\s\d{3}\s\d{3}\s\d{4}$", phone_number):
        return True

    '''check number if is this format: # (###) ###-####'''
    if  re.match("^\d{1}\s\(\d{3}\)\s\d{3}-\d{4}$", phone_number):
        return True

    '''check number if is this format: +32 (##) ###-####'''
    if  re.match("^\+\d{2}\s\(\d{2}\)\s\d{3}-\d{4}$", phone_number):
        return True
   
    '''check number if is this format: ### ### ### ####'''
    if  re.match("^\d{3}\s\d{3}\s\d{3}\s\d{4}$", phone_number):
        return True
    
    ''''check number if is this format: ###-####'''
    if  re.match("^\d{3}-\d{4}$", phone_number):
        return True
    
    '''check number if is in this format: # (###) ###-####'''
    if  re.match("^\d{1}\s\(\d{3}\)\s\d{3}-\d{4}$", phone_number):
        return True
    
    '''check number if is in this format: +# (###) ###-####'''
    if  re.match("^\+\d{1}\s\(\d{3}\)\s\d{3}-\d{4}$", phone_number):
        return True
    
    '''check number if is in this format: ###'''
    if  re.match("^\d{3}$", phone_number):
        return False
    
    '''check number if is in this format: #/###/###/####'''
    if  re.match("^\d{1}\/\d{3}\/\d{3}\/\d{4}$", phone_number):
        return False
    
    '''check number if is in this format: (###) ###-#### ext ###'''
    if  re.match("^\(\d{3}\)\s\d{3}-\d{4}\sext\s\d{3}$", phone_number):
        return False
    
    '''check number if is in this format: +## (###) ###-####'''
    if  re.match("^\+\d{2}\s\(\d{3}\)\s\d{3}-\d{4}$", phone_number):
        return False
    
    '''check number if is in this format: Nr ###-###-####'''
    if  re.match("^Nr\s\d{3}-\d{3}-\d{4}$", phone_number):
        return False
    
    '''check number if is in this format: ##########'''
    if  re.match("^\d{10}$", phone_number):
        return False
    
    '''check number if is in this format: +#### (###) ###-####'''
    if re.match("^\+\d{4}\s\(\d{3}\)\s\d{3}-\d{4}$", phone_number):
        return False

    '''check number if is in this format: (###) ###-####'''
    if re.match("^\(\d{3}\)\s\d{3}-\d{4}$", phone_number):
        return False
    
    '''check number if is in this format: <###> ###-####'''
    if re.match("^\<\d{3}\>\s\d{3}-\d{4}$", phone_number):
        return False
        
    if re.match("/(\+\d{1,3}\s?)?((\(\d{3}\)\s?)|(\d{3})(\s|-?))(\d{3}(\s|-?))(\d{4})(\s?(([E|e]xt[:|.|]?)|x|X)(\s?\d+))?/g", phone_number):
        return True

# Create the Pydantic model class for request and response data
class Person(BaseModel):
    full_name: str
    phone_number: str

# Define the API endpoints

# Function to write to the audit log
def write_to_audit_log(db, event_type, event_data):
    audit_log_entry = AuditLog(event_type=event_type, event_data=event_data)
    db.add(audit_log_entry)
    db.commit()

@app.get("/PhoneBook/list")
def list_phonebook():
    # Get a new session for PhoneBook
    phonebook_session = PhoneBookSession()
    # Query all the records in the phonebook table
    phonebook = phonebook_session.query(PhoneBook).all()
    # Close the session for PhoneBook
    phonebook_session.close()

    # Return the list of records as JSON objects
    return phonebook

@app.post("/PhoneBook/add")
def add_person(person: Person):
    # Get a new session for PhoneBook
    phonebook_session = PhoneBookSession()

    # Validate name and phone number
    if name_check(person.full_name) == False:
        phonebook_session.close()
        raise HTTPException(status_code=400, detail="Invalid name")
    if phone_check(person.phone_number) == False:
        phonebook_session.close()
        raise HTTPException(status_code=400, detail="Invalid phone number")

    # Check if the phone number already exists in the database
    existing_person = phonebook_session.query(PhoneBook).filter_by(phone_number=person.phone_number).first()
    if existing_person:
        phonebook_session.close()
        raise HTTPException(status_code=400, detail="Person already exists in the database")

    # Otherwise, create a new PhoneBook record and add it to the database
    new_person = PhoneBook(full_name=person.full_name, phone_number=person.phone_number)
    phonebook_session.add(new_person)
    phonebook_session.commit()

    # Write to the audit log
    write_to_audit_log(AuditLogSession(), "add_person", f"full_name={person.full_name}, phone_number={person.phone_number}")

    # Close the session for PhoneBook
    phonebook_session.close()

    # Return a success message
    return {"message": "Person added successfully"}

@app.put("/PhoneBook/deleteByName")
def delete_by_name(full_name: str):
    # Validate the name
    if name_check(full_name) == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid name")
    
    # Get a new session
    session = PhoneBookSession()
    # Query the person by name in the database
    person = session.query(PhoneBook).filter_by(full_name=full_name).first()
    # If the person does not exist, raise an exception
    if not person:
        session.close()
        raise HTTPException(status_code=404, detail="Person not found in the database")
    # Otherwise, delete the person from the database
    session.delete(person)
    
    session.commit()
    # Close the session
    write_to_audit_log(AuditLogSession(), "delete_by_name", f"full_name={full_name}")
    session.close()
    # Return a success message
    return {"message": "Person deleted successfully"}

@app.put("/PhoneBook/deleteByNumber")
def delete_by_number(phone_number: str):
    # Validate the phone number
    if phone_check(phone_number) == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid phone number")
    # Get a new session
    session = PhoneBookSession()
    # Query the person by phone number in the database
    person = session.query(PhoneBook).filter_by(phone_number=phone_number).first()
    # If the person does not exist, raise an exception
    if not person:
        session.close()
        raise HTTPException(status_code=404, detail="Person not found in the database")
    # Otherwise, delete the person from the database
    session.delete(person)
    session.commit()
    write_to_audit_log(AuditLogSession(), "delete_by_number", f"phone_number={phone_number}")
    # Close the session

    session.close()
    # Return a success message
    return {"message": "Person deleted successfully"}