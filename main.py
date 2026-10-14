from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
import requests
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class StudentCreate(BaseModel):
    name: str
    dob: str
    contact: str
class AskQuery(BaseModel):
 question: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the EWB Students CRUD API"}

@app.post("/students")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    
    new_student = models.Student(name=student.name, dob=student.dob, contact=student.contact)
    db.add(new_student)    
    db.commit()            
    db.refresh(new_student) 
    return new_student
@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return students

@app.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        return {"error": "Student not found"}
    return student

@app.put("/students/{student_id}")
def update_student(student_id: int, student_data: StudentCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        return {"error": "Student not found"}
    
    student.name = student_data.name
    student.dob = student_data.dob
    student.contact = student_data.contact
    db.commit()
    db.refresh(student)
    return student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        return {"error": "Student not found"}
    
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}

@app.post("/ask")
def ask_ai(query: AskQuery, db: Session = Depends(get_db)):
    
    students = db.query(models.Student).all()
    if not students:
        return{"answer": "the database is currently empty. There are 0 students."}
    
    context = "Student Database Records:\n"
    for s in students:
        context += f"ID: {s.id}, Name: {s.name}, DOB: {s.dob}, Contact: {s.contact}\n"
        

    prompt = f"{context}\n\nQuestion: {query.question}\nAnswer the question based ONLY on the student records provided above. Keep it short."
    
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3.2:1b",
            "prompt": prompt,
            "stream": False
        })
        return {"answer": response.json()["response"]}
    except Exception as e:
        return {"error": f"AI connection failed. Make sure Ollama is running! Details: {str(e)}"}