import logging

from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest
from src.models.db import db_session
from src.models.sesion import EstadoSesionEnum, Sesion
from src.utils.str_utils import str_none_or_empty


logger = logging.getLogger(__name__)


class AsignarPlan(BaseCommand):
    def __init__(self, **info):

        if str_none_or_empty(info.get('id_plan_deportista')):
            logger.error("ID Plan deportista es obligatorio")
            raise BadRequest

        if str_none_or_empty(info.get('fecha_sesion')):
            logger.error("Fecha sesion es obligatoria")
            raise BadRequest

        self.id_plan_deportista = info.get('id_plan_deportista')
        self.fecha_sesion = info.get('fecha_sesion')

    def execute(self):
        logger.info("Asignando plan")

        sesion: Sesion = Sesion(
            id_plan_deportista=self.id_plan_deportista,
            fecha_inicio=self.fecha_sesion,
            estado='agendada')

        db_session.add(sesion)
        db_session.commit()
        logger.info(f'Sesion asignada {sesion.id}')

        resp = {
            'id_sesion': str(sesion.id),
        }

        return resp
