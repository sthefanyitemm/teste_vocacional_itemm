from flask.views import MethodView

class notFoundController(MethodView):
    def get(self,error):
        return f"Pagina não encontrada {error}"
