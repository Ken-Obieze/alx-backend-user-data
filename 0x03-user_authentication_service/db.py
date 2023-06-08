#!/usr/bin/env python3
"""DB module."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class DB:
    """DB class."""

    def __init__(self) -> None:
        """Initialize a new DB instance."""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database.
        Args:
            email: Email of the user
            hashed_password: Hashed password of the user
        Returns:
            User object of the newly created user
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user in the database based on the provided filters.
        Args:
            **kwargs: Arbitrary keyword arguments representing the filters
        Returns:
            User object of the found user
        Raises:
            NoResultFound: If no results are found
            InvalidRequestError: If wrong query arguments are passed
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except InvalidRequestError:
            raise InvalidRequestError

        def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes in the database.
        Args:
            user_id: ID of the user to update
            **kwargs: Arbitrary keyword arguments representing the attributes to update.
        Raises:
            ValueError: If an argument that does not correspond to a user attribute is passed
        """
        try:
            user = self.find_user_by(id=user_id)
            for attr, value in kwargs.items():
                if hasattr(user, attr):
                    setattr(user, attr, value)
                else:
                    raise ValueError
            self._session.commit()
        except NoResultFound:
            raise NoResultFound
