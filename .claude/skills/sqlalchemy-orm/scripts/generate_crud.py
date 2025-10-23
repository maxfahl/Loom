import argparse
import os
from datetime import datetime

def generate_crud_file(model_name: str, output_dir: str):
    """
    Generates a basic CRUD (Create, Read, Update, Delete) Python file
    for a given SQLAlchemy model.

    Args:
        model_name: The name of the SQLAlchemy model (e.g., "User", "Product").
        output_dir: The directory where the CRUD file will be saved.
    """

    file_name = f"crud_{model_name.lower()}.py"
    output_path = os.path.join(output_dir, file_name)

    content = f"""
from sqlalchemy.orm import Session
from typing import List, Optional

# Assuming your models are in a 'models' module or similar
# from .models import {model_name} # Adjust import as needed

# Placeholder for your actual model import
class {model_name}:
    # This is a placeholder. Replace with your actual SQLAlchemy model definition.
    # Example: id: int, name: str, etc.
    id: int
    name: str
    # Add other attributes as per your model

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"<{model_name}(id={{self.id}}, name='{{self.name}}')>"


# --- Create ---
def create_{model_name.lower()}(db: Session, item_data: dict) -> {model_name}:
    db_item = {model_name}(**item_data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# --- Read ---
def get_{model_name.lower()}(db: Session, item_id: int) -> Optional[{model_name}]:
    return db.query({model_name}).filter({model_name}.id == item_id).first()

def get_all_{model_name.lower()}s(db: Session, skip: int = 0, limit: int = 100) -> List[{model_name}]:
    return db.query({model_name}).offset(skip).limit(limit).all()

# --- Update ---
def update_{model_name.lower()}(db: Session, item_id: int, item_data: dict) -> Optional[{model_name}]:
    db_item = db.query({model_name}).filter({model_name}.id == item_id).first()
    if db_item:
        for key, value in item_data.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

# --- Delete ---
def delete_{model_name.lower()}(db: Session, item_id: int) -> Optional[{model_name}]:
    db_item = db.query({model_name}).filter({model_name}.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
"""

    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(content)
    print(f"Generated CRUD file: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a basic CRUD (Create, Read, Update, Delete) Python file for a SQLAlchemy model."
    )
    parser.add_argument(
        "--model_name",
        type=str,
        required=True,
        help="Name of the SQLAlchemy model (e.g., 'User', 'Product')."
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=".",
        help="Directory to save the generated CRUD file. Defaults to current directory."
    )

    args = parser.parse_args()

    generate_crud_file(args.model_name, args.output_dir)
