"""
Módulo para lidar com serviços relacionados a tipos.
"""
from db import db
from models.auction import Auction
from models.type import Type
from sqlalchemy import asc, desc


class TypeService:
    """
    Classe de serviço para operações relacionadas a tipos.
    """

    @staticmethod
    def create_type(data):
        """
        Cria um novo tipo.

        Args:
            data (dict): Dados contendo os detalhes do tipo.

        Returns:
            Type: O objeto tipo criado.
        """
        new_type = Type(
            name=data['name'],
            description=data['description']
        )

        db.session.add(new_type)
        db.session.commit()

        return new_type

    @staticmethod
    def get_all_types(page=None, per_page=None, order_by='id', order_asc=False, order_desc=False):
        """
        Recupera os tipos com ordenação, com paginação opcional.

        Args:
            page (int, opcional): Número da página. Se None, retorna todos os resultados.
            per_page (int, opcional): Número de itens por página. Se None, retorna todos os resultados.
            order_by (str): Campo para ordenar ('id' ou 'name').
            order_asc (bool): Se deve ordenar em ordem crescente.
            order_desc (bool): Se deve ordenar em ordem decrescente.

        Returns:
            Objeto de paginação, se a paginação estiver ativada, caso contrário, uma lista de objetos Type.
        """
        if order_by not in ['id', 'name']:
            raise ValueError("Valor inválido para 'order_by'. Use 'id' ou 'name'.")

        if order_asc and order_desc:
            raise ValueError("Não é possível definir tanto 'order_asc' quanto 'order_desc' como True.")

        query = Type.query

        if order_asc:
            query = query.order_by(asc(getattr(Type, order_by)))
        elif order_desc:
            query = query.order_by(desc(getattr(Type, order_by)))
        else:
            query = query.order_by(asc(Type.id))  # Ordem padrão

        if page is None or per_page is None:
            return query.all()

        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get_type_by_id(type_id):
        """
        Recupera um tipo pelo ID.

        Args:
            type_id (int): O ID do tipo.

        Returns:
            Type: O objeto tipo se encontrado, caso contrário None.
        """
        return Type.query.get(type_id)

    @staticmethod
    def update_type(type_id, data):
        """
        Atualiza um tipo existente.

        Args:
            type_id (int): O ID do tipo a ser atualizado.
            data (dict): Dados contendo os campos atualizados.

        Returns:
            Type: O objeto tipo atualizado se encontrado, caso contrário None.
        """
        type_obj = Type.query.get(type_id)
        if not type_obj:
            return None

        if 'name' in data:
            type_obj.name = data['name']
        if 'description' in data:
            type_obj.description = data['description']

        db.session.commit()
        return type_obj

    @staticmethod
    def delete_type(type_id):
        """
        Deleta um tipo pelo ID, somente se não houver leilões associados.

        Args:
            type_id (int): O ID do tipo.

        Returns:
            dict: {'success': True} se deletado, {'error': 'mensagem'} se não encontrado ou se houver dependências.
        """
        type_obj = Type.query.get(type_id)
        if not type_obj:
            return {'error': 'Tipo não encontrado'}

        associated_auctions = Auction.query.filter_by(type_id=type_id).first()
        if associated_auctions:
            return {'error': 'Não é possível deletar o tipo. Há leilões associados.'}

        db.session.delete(type_obj)
        db.session.commit()
        return {'success': True}
