from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey
from typing import List





class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)


#CREATE USER DATABASE:
class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
# This creates one URL dict key with multiple URL links, Parent connection:
    urls: Mapped[List["Urls"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Urls(UserMixin, db.Model):
    __tablename__ = 'urls'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url_address: Mapped[str] = mapped_column(String(350), unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
# Create the relationship with Users:
    #This is the child connection to Users:
    user: Mapped["Users"] = relationship(back_populates="urls")
    #This opens the parent connection to Shops:
    shop_name: Mapped["Shops"] = relationship(back_populates="url", cascade="all, delete-orphan")

"""Reasoning for adding shop name abbreviations - When adding the shop locations to the database, I would like to add
the shop/URLs id as well to help the user identify which shop it is from as some multiple shops can have the same location. 
Thus, when adding items to database and searching the shop location in database it would allocate the wrong id, which would
give the user incorrect data for processing."""

class Shops(UserMixin, db.Model):
    __tablename__ = 'shops'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    shop_name: Mapped[str] = mapped_column(String(250), nullable=False)
    url_id: Mapped[int] = mapped_column(ForeignKey("urls.id"))
    # Relationship:
    ## This is the child connection to Urls:
    url: Mapped["Urls"] = relationship(back_populates="shop_name")
    ## This is the parent connection to ShopLoc:
    loc: Mapped[List["ShopLoc"]] = relationship(back_populates="shops", cascade="all, delete-orphan")


class ShopLoc(UserMixin, db.Model):
    __tablename__ = 'shop_loc'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    shop_loc: Mapped[str] = mapped_column(String(250), nullable=False)
    shop_id: Mapped[int] = mapped_column(ForeignKey("shops.id"))
    # Relationships:
    ##This is the child connection to Shops:
    shops: Mapped["Shops"] = relationship(back_populates="loc")
    ##This is the parent connection to ItemData:
    items: Mapped[List["ItemData"]] = relationship(back_populates="shop", cascade="all, delete-orphan")


class ItemData(db.Model):
    __tablename__ = 'item_data'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    shop_name: Mapped[String] = mapped_column(String(250), nullable=False)
    customer: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    product_id: Mapped[str] = mapped_column(String(250), nullable=False)
    qty: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    subtotal: Mapped[int] = mapped_column(Integer, nullable=False)
    loc_id: Mapped[int] = mapped_column(ForeignKey("shop_loc.id"))
    #Relationships:
      #This is the child connection to Shops:
    shop: Mapped["ShopLoc"] = relationship(back_populates="items")
