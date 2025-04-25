"""modify_book_id_autoincrement

Revision ID: a9bd27f3ac00
Revises: 
Create Date: 2025-04-25 14:34:10.000451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9bd27f3ac00'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade()->None:
    # Créer une séquence pour l'auto-incrémentation
    op.execute("CREATE SEQUENCE IF NOT EXISTS books_id_seq")
    
    # Modifier la colonne id pour utiliser la séquence
    op.execute("ALTER TABLE books ALTER COLUMN id SET DEFAULT nextval('books_id_seq')")
    op.execute("ALTER TABLE books ALTER COLUMN id SET NOT NULL")
    
    # Ajuster la séquence pour qu'elle démarre après la plus grande valeur d'id existante
    op.execute("SELECT setval('books_id_seq', COALESCE((SELECT MAX(id) FROM books), 0) + 1, false)")


def downgrade()->None:
    # Retirer la valeur par défaut
    op.execute("ALTER TABLE books ALTER COLUMN id DROP DEFAULT")
    
    # Optionnel: supprimer la séquence si vous voulez revenir complètement en arrière
    op.execute("DROP SEQUENCE IF EXISTS books_id_seq")