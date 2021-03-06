"""followers

Revision ID: 74bc3e566675
Revises: 28fab7031fb0
Create Date: 2021-09-17 19:53:04.042609

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "74bc3e566675"
down_revision = "28fab7031fb0"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "followers",
        sa.Column("follower_id", sa.Integer(), nullable=True),
        sa.Column("followed_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["followed_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["follower_id"],
            ["user.id"],
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("followers")
    # ### end Alembic commands ###
