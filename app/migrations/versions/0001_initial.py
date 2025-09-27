from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('role', sa.Enum('user','admin','org_admin', name='roleenum'), server_default='user'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    op.create_table('organizations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('owner_user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('branding_json', sa.JSON(), server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    op.create_table('pets',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('org_id', sa.Integer(), sa.ForeignKey('organizations.id')),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('species', sa.String(), server_default='dog'),
        sa.Column('breed', sa.String(), server_default='unknown'),
        sa.Column('meta_json', sa.JSON(), server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    op.create_table('stories',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('org_id', sa.Integer(), sa.ForeignKey('organizations.id')),
        sa.Column('pet_id', sa.Integer(), sa.ForeignKey('pets.id')),
        sa.Column('title', sa.String(), server_default='Untitled'),
        sa.Column('status', sa.String(), server_default='draft'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    op.create_table('story_revisions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('story_id', sa.Integer(), sa.ForeignKey('stories.id')),
        sa.Column('script_text', sa.String(), server_default=''),
        sa.Column('voice_pack_id', sa.Integer(), nullable=True),
        sa.Column('style_json', sa.JSON(), server_default='{}'),
        sa.Column('duration_sec', sa.Integer(), server_default=30),
        sa.Column('render_status', sa.String(), server_default='pending'),
        sa.Column('job_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    op.create_table('assets',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('owner_org_id', sa.Integer(), sa.ForeignKey('organizations.id')),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('s3_key', sa.String(), unique=True, nullable=False),
        sa.Column('cdn_url', sa.String(), nullable=True),
        sa.Column('duration', sa.Integer(), server_default='0'),
        sa.Column('width', sa.Integer(), server_default='0'),
        sa.Column('height', sa.Integer(), server_default='0'),
        sa.Column('checksum', sa.String(), server_default=''),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )

def downgrade() -> None:
    op.drop_table('assets')
    op.drop_table('story_revisions')
    op.drop_table('stories')
    op.drop_table('pets')
    op.drop_table('organizations')
    op.drop_table('users')
