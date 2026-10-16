"""Lecturas sin efectos de escritura."""
def por_estado(repo,estado): return [c for c in repo.listar() if c.estado==estado]
def por_sucursal(repo,sucursal): return [c for c in repo.listar() if c.sucursal_id==sucursal]
def por_medico(repo,medico): return [c for c in repo.listar() if c.medico_id==medico]
