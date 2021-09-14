"""empty message

Revision ID: 663535b0be04
Revises: 6e485b682d29
Create Date: 2021-09-14 23:51:21.725645

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '663535b0be04'
down_revision = '6e485b682d29'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('prescription',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('appointment_id', sa.Integer(), nullable=True),
    sa.Column('doctor_id', sa.Integer(), nullable=True),
    sa.Column('medication_id', sa.Integer(), nullable=True),
    sa.Column('dose', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['appointment_id'], ['patient.id'], ),
    sa.ForeignKeyConstraint(['doctor_id'], ['appointment.id'], ),
    sa.ForeignKeyConstraint(['medication_id'], ['medicine.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('medicine', sa.Column('price', sa.Integer(), nullable=False))
    op.drop_column('medicine', 'dose')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('medicine', sa.Column('dose', mysql.SMALLINT(), autoincrement=False, nullable=False))
    op.drop_column('medicine', 'price')
    op.drop_table('prescription')
    # ### end Alembic commands ###