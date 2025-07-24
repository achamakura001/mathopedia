"""Update grade_level to support competitive exams

Revision ID: 6ffad2e996d6
Revises: 99b412ad6b8d
Create Date: 2025-06-28 13:45:40.208298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ffad2e996d6'
down_revision = '99b412ad6b8d'
branch_labels = None
depends_on = None


def upgrade():
    # Add new column as string
    op.add_column('questions', sa.Column('grade_level_new', sa.String(50), nullable=True))
    
    # Update the new column with converted values from the old column
    connection = op.get_bind()
    connection.execute(sa.text("UPDATE questions SET grade_level_new = CAST(grade_level AS CHAR)"))
    
    # Drop the old column
    op.drop_column('questions', 'grade_level')
    
    # Rename the new column
    op.alter_column('questions', 'grade_level_new', new_column_name='grade_level')
    
    # Make it non-nullable
    op.alter_column('questions', 'grade_level', nullable=False)


def downgrade():
    # Add new column as integer
    op.add_column('questions', sa.Column('grade_level_new', sa.Integer(), nullable=True))
    
    # Update the new column with converted values from the old column (only numeric values)
    connection = op.get_bind()
    connection.execute(sa.text("UPDATE questions SET grade_level_new = CAST(grade_level AS UNSIGNED) WHERE grade_level REGEXP '^[0-9]+$'"))
    
    # Drop the old column
    op.drop_column('questions', 'grade_level')
    
    # Rename the new column
    op.alter_column('questions', 'grade_level_new', new_column_name='grade_level')
    
    # Make it non-nullable
    op.alter_column('questions', 'grade_level', nullable=False)
