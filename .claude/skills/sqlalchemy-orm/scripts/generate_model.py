import argparse
import os
from datetime import datetime

def generate_model_file(table_name: str, columns: list[str], output_dir: str):
    """
    Generates a SQLAlchemy 2.0 declarative model Python file.

    Args:
        table_name: The name of the table (and class).
        columns: A list of column definitions in the format "name:type:constraints".
                 Example: "id:int:pk,name:str:unique,email:str"
        output_dir: The directory where the model file will be saved.
    """

    model_name = ''.join([part.capitalize() for part in table_name.split('_')])
    file_name = f"{table_name.lower().replace(' ', '_')}_model.py"
    output_path = os.path.join(output_dir, file_name)

    imports = [
        "from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey",
        "from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship",
        "from typing import Optional, List",
        "from datetime import datetime"
    ]

    column_definitions = []
    relationships = []

    for col_str in columns:
        parts = col_str.split(':')
        col_name = parts[0]
        col_type_str = parts[1].lower()
        col_constraints = parts[2:]

        # Map string types to SQLAlchemy types and Python types
        sqla_type = "String"
        python_type = "str"
        default_value = ""

        if col_type_str == "int":
            sqla_type = "Integer"
            python_type = "int"
        elif col_type_str == "bool":
            sqla_type = "Boolean"
            python_type = "bool"
        elif col_type_str == "float":
            sqla_type = "Float"
            python_type = "float"
        elif col_type_str == "datetime":
            sqla_type = "DateTime"
            python_type = "datetime"
            default_value = "default=datetime.utcnow"

        # Handle constraints
        constraints = []
        if "pk" in col_constraints:
            constraints.append("primary_key=True")
        if "unique" in col_constraints:
            constraints.append("unique=True")
        if "nullable" not in col_constraints and "pk" not in col_constraints:
            constraints.append("nullable=False")
        if "fk" in col_constraints:
            fk_table, fk_col = col_constraints[col_constraints.index("fk") + 1].split('.')
            constraints.append(f"ForeignKey('{fk_table}.{fk_col}')")
            # Add a basic relationship for FKs
            related_model_name = ''.join([part.capitalize() for part in fk_table.split('_')])
            relationships.append(
                f"    {fk_table}: Mapped[\"{related_model_name}\"] = relationship(back_populates=\" \")"
            )

        sqla_col_def = f"Column({sqla_type}, {', '.join(constraints)})"

        # Mapped column definition
        if "pk" in col_constraints:
            column_definitions.append(f"    {col_name}: Mapped[{python_type}] = mapped_column({sqla_type}, primary_key=True)")
        elif "fk" in col_constraints:
            column_definitions.append(f"    {col_name}: Mapped[{python_type}] = mapped_column({sqla_type}, {', '.join(constraints)})")
        else:
            column_definitions.append(f"    {col_name}: Mapped[{python_type}] = mapped_column({sqla_type}, {', '.join(constraints)})")

    # Add a default Base if not already present (for standalone generation)
    model_content = f"""
{'
'.join(imports)}

Base = declarative_base()

class {model_name}(Base):
    __tablename__ = '{table_name.lower()}'

{'
'.join(column_definitions)}
{'
'.join(relationships)}

    def __repr__(self):
        return f"<{model_name}(id={{self.id}}, name='{{self.name}}')>"
"""

    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(model_content)
    print(f"Generated model file: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a SQLAlchemy 2.0 declarative model Python file."
    )
    parser.add_argument(
        "--table_name",
        type=str,
        required=True,
        help="Name of the table (and class), e.g., User, Product."
    )
    parser.add_argument(
        "--columns",
        type=str,
        nargs='+',
        required=True,
        help="Column definitions in 'name:type:constraints' format. "
             "Constraints: pk, unique, nullable, fk:other_table.other_col. "
             "Example: 'id:int:pk', 'name:str:unique', 'email:str', 'user_id:int:fk:users.id'"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=".",
        help="Directory to save the generated model file. Defaults to current directory."
    )

    args = parser.parse_args()

    generate_model_file(args.table_name, args.columns, args.output_dir)
