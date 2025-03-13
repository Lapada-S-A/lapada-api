from db import db
from models.category import Category
from sqlalchemy import asc, desc

class CategoryService:
    """
    Classe de serviço para operações relacionadas a categorias.
    """
    
    @staticmethod
    def create_category(data):
        """
        Cria uma nova categoria.

        Args:
            data (dict): Dados contendo os detalhes da categoria.

        Returns:
            Category: O objeto da categoria criada.
        """
        category = Category(
            name=data['name']
        )
        
        db.session.add(category)
        db.session.commit()
        
        return category
    
    @staticmethod
    def get_all_categories(page, per_page, order_by, order_asc, order_desc):
        """
        Recupera categorias paginadas com ordenação.

        Args:
            page (int): Número da página.
            per_page (int): Número de itens por página.
            order_by (str): Campo para ordenar ('id' ou 'name').
            order_asc (bool): Se a ordenação será ascendente.
            order_desc (bool): Se a ordenação será descendente.

        Returns:
            Pagination object with categories.
        """
        if order_by not in ['id', 'name']:
            raise ValueError("Valor inválido para 'order_by'. Use 'id' ou 'name'.")

        if order_asc and order_desc:
            raise ValueError("Não é possível definir 'order_asc' e 'order_desc' como verdadeiros ao mesmo tempo.")

        query = Category.query

        if order_asc:
            query = query.order_by(asc(getattr(Category, order_by)))
        elif order_desc:
            query = query.order_by(desc(getattr(Category, order_by)))
        else:
            query = query.order_by(asc(Category.id))  # Ordem padrão

        if page is None or per_page is None:
            return query.all()

        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get_category_by_id(category_id):
        """
        Recupera uma categoria pelo seu ID.

        Args:
            category_id (int): O ID da categoria.

        Returns:
            Category: O objeto da categoria se encontrado, senão None.
        """
        return Category.query.get(category_id)

    @staticmethod
    def update_category(category_id, data):
        """
        Atualiza os detalhes de uma categoria.

        Args:
            category_id (int): O ID da categoria a ser atualizada.
            data (dict): Dicionário contendo os detalhes atualizados da categoria.

        Returns:
            dict: {'success': True} se atualizado, {'error': 'mensagem'} se não encontrado.
        """
        category = Category.query.get(category_id)
        if not category:
            return {'error': 'Categoria não encontrada'}

        if 'name' in data:
            category.name = data['name']

        db.session.commit()
        return {'success': True, 'category': category.to_dict()}

    @staticmethod
    def delete_category(category_id):
        """
        Deleta uma categoria apenas se não tiver leilões associados.

        Args:
            category_id (int): O ID da categoria.

        Returns:
            dict: {'success': True} se deletado, {'error': 'mensagem'} se não encontrado ou se houver dependências.
        """
        category = Category.query.get(category_id)
        if not category:
            return {'error': 'Categoria não encontrada'}

        # Verifica se há leilões associados
        if category.auctions:
            return {'error': 'Não é possível deletar a categoria. Existem leilões associados.'}

        db.session.delete(category)
        db.session.commit()
        return {'success': True}
