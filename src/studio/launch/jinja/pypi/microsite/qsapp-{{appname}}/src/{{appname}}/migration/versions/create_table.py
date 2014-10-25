from sqlalchemy import sql
from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        u'channel',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.Unicode(64), nullable=False, unique=True, index=True),
        sa.Column('introduction', sa.Unicode(1024), nullable=True),
        sa.Column('date_created', sa.DateTime(timezone=True),
                    nullable=False, index=True,
                    server_default=sa.func.current_timestamp()),
    )

    op.create_table(
        u'article',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('channel_id', sa.Integer(), nullable=False, index=True),
        sa.Column('is_sticky', sa.Boolean(),
                    server_default=sql.false(), nullable=False),
        sa.Column('title', sa.Unicode(64), nullable=False, unique=True, index=True),
        sa.Column('date_published', sa.DateTime(timezone=True),
                    nullable=False, index=True,
                    server_default=sa.func.current_timestamp()),
        sa.Column('date_created', sa.DateTime(timezone=True),
                    nullable=False, index=True,
                    server_default=sa.func.current_timestamp()),
    )

    op.create_table(
        u'article_content',
        sa.Column('id', sa.Integer(), sa.ForeignKey('article.id'),
                    nullable=False, primary_key=True),
        sa.Column('content', sa.UnicodeText(), nullable=False),
    )


def downgrade():
    op.drop_table(u'article_content')
    op.drop_table(u'article')
    op.drop_table(u'channel')
