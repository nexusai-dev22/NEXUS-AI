from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    nombre = Column(
        String(100),
        nullable=False,
    )

    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    creado_en = Column(
        DateTime,
        default=datetime.utcnow,
    )

    conversaciones = relationship(
        "Conversation",
        back_populates="usuario",
        cascade="all, delete-orphan",
    )

    memorias = relationship(
        "Memory",
        back_populates="usuario",
        cascade="all, delete-orphan",
    )


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    usuario_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    titulo = Column(
        String(255),
        nullable=False,
        default="Nueva conversación",
    )

    creado_en = Column(
        DateTime,
        default=datetime.utcnow,
    )

    usuario = relationship(
        "User",
        back_populates="conversaciones",
    )

    mensajes = relationship(
        "Message",
        back_populates="conversacion",
        cascade="all, delete-orphan",
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id"),
        nullable=False,
        index=True,
    )

    rol = Column(
        String(20),
        nullable=False,
    )

    contenido = Column(
        Text,
        nullable=False,
    )

    creado_en = Column(
        DateTime,
        default=datetime.utcnow,
    )

    conversacion = relationship(
        "Conversation",
        back_populates="mensajes",
    )


class Memory(Base):
    __tablename__ = "memories"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    usuario_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    tipo = Column(
        String(50),
        nullable=False,
        default="general",
    )

    clave = Column(
        String(100),
        nullable=False,
    )

    valor = Column(
        Text,
        nullable=False,
    )

    creado_en = Column(
        DateTime,
        default=datetime.utcnow,
    )

    actualizado_en = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    usuario = relationship(
        "User",
        back_populates="memorias",
    )
