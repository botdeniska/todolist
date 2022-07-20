from typing import Optional, Generator, List, Dict, Any
from contextlib import contextmanager

from sqlalchemy import create_engine, Integer, String, Column, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base


engine = create_engine('sqlite:///tasks.db')
LocalSession = sessionmaker(bind=engine, expire_on_commit=False)
Base: DeclarativeMeta = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(String(500))
    date = Column(DateTime, nullable=True)
    is_done = Column(Boolean, default=False)

    def as_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date.isoformat(),
            'is_done': self.is_done
        }


def init_db() -> None:
    Base.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()


def get_all_tasks(session: Session) -> List[Task]:
    return session.query(Task).all()


def get_task(session: Session, id_: int) -> Optional[Task]:
    return session.get(Task, id_)


def add_task(session: Session, instance: Task) -> int:
    session.add(instance)
    session.commit()
    return instance.id


def delete_task(session: Session, id_: int) -> bool:
    if session.query(Task).filter(Task.id == id_).delete(synchronize_session="fetch"):
        session.commit()
        return True
    return False


def change_task_status(session: Session, id_: int, status: bool) -> bool:
    if session.query(Task).filter(Task.id == id_).update(
            {"is_done": status}, synchronize_session="fetch"
    ):
        session.commit()
        return True
    return False

