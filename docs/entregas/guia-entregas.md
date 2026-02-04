# Como Entregar tus Ejercicios

Esta guia te explica **paso a paso** como subir tu trabajo. No necesitas saber Git, solo sigue las instrucciones.

---

## Resumen Rapido

```
Tu computadora → Tu fork en GitHub → Pull Request al profesor
```

Suena complicado, pero son solo **5 pasos** que haras siempre igual.

---

## Paso 1: Crear tu copia del repositorio (solo la primera vez)

Esto se llama "hacer un fork". Es como fotocopiar un libro para poder escribir en tu copia.

1. Abre: [https://github.com/TodoEconometria/ejercicios-bigdata](https://github.com/TodoEconometria/ejercicios-bigdata)
2. Arriba a la derecha, haz clic en el boton **"Fork"**
3. GitHub te preguntara donde crear la copia. Deja todo como esta y haz clic en **"Create fork"**
4. Espera unos segundos. Ahora tienes tu propia copia en `github.com/TU_USUARIO/ejercicios-bigdata`

!!! success "Solo haces esto UNA vez"
    El fork es tuyo para siempre. No lo borres.

---

## Paso 2: Descargar tu copia a tu computadora (solo la primera vez)

1. En TU fork (no el del profesor), haz clic en el boton verde **"Code"**
2. Copia la URL que aparece (empieza con `https://github.com/TU_USUARIO/...`)
3. Abre una terminal (CMD en Windows, Terminal en Mac)
4. Escribe estos comandos:

```bash
cd Documentos
git clone https://github.com/TU_USUARIO/ejercicios-bigdata.git
cd ejercicios-bigdata
```

Cambia `TU_USUARIO` por tu nombre de usuario de GitHub.

!!! info "Ahora tienes la carpeta en tu computadora"
    Busca en `Documentos/ejercicios-bigdata/`. Ahi trabajaras.

---

## Paso 3: Crear tu carpeta de entrega

Dentro de la carpeta del repositorio, busca donde va tu entrega. Por ejemplo:

- Ejercicio 1.1 SQLite → `entregas/01_bases_de_datos/1.1_sqlite/`
- Ejercicio 2.1 PostgreSQL → `entregas/01_bases_de_datos/2.1_postgresql_hr/`
- Trabajo Final → `entregas/trabajo_final/`

**Crea una carpeta con tu nombre** dentro de la carpeta del ejercicio:

```
entregas/01_bases_de_datos/1.1_sqlite/garcia_maria/
```

!!! warning "Formato del nombre de carpeta"
    - Todo en **minusculas**
    - Sin tildes ni espacios
    - Formato: `apellido_nombre`
    - Ejemplo: `garcia_maria`, `lopez_juan`, `martinez_ana`

**Pon tus archivos dentro de tu carpeta:**

```
entregas/01_bases_de_datos/1.1_sqlite/garcia_maria/
├── mi_solucion.py
├── consultas.sql
└── REFLEXION.md
```

---

## Paso 4: Subir tu trabajo a GitHub

Abre la terminal en la carpeta del repositorio y ejecuta estos 4 comandos:

```bash
git add .
git commit -m "Entrega 1.1 - Maria Garcia"
git push
```

!!! tip "Que significa cada comando"
    - `git add .` → Prepara todos tus archivos nuevos
    - `git commit -m "..."` → Guarda los cambios con un mensaje
    - `git push` → Sube todo a tu GitHub

Si te pide usuario y contrasena, usa tu cuenta de GitHub.

---

## Paso 5: Pedir que el profesor revise tu trabajo (Pull Request)

Este es el paso final. Le dices al profesor "ya termine, revisame".

1. Ve a tu fork en GitHub: `github.com/TU_USUARIO/ejercicios-bigdata`
2. Veras un mensaje amarillo que dice algo como "This branch is 1 commit ahead"
3. Haz clic en **"Contribute"** → **"Open pull request"**
4. Escribe un titulo claro: `[1.1] Garcia Maria - Ejercicio SQLite`
5. Haz clic en **"Create pull request"**

!!! success "Listo!"
    El profesor recibira tu entrega y la revisara.

---

## Para la siguiente entrega

Ya tienes el fork y el repositorio descargado. Solo repite los pasos 3, 4 y 5:

1. Crea tu carpeta en el nuevo ejercicio
2. Pon tus archivos
3. Ejecuta `git add .`, `git commit`, `git push`
4. Crea el Pull Request

---

## Problemas comunes

### "Mi PR tiene 30+ commits que no son mios"

Esto pasa cuando tu fork esta desactualizado. Lee esta guia: [Como crear un PR limpio](../git-github/pr-limpio.md)

### "Git me dice que hay conflictos"

Tu fork esta muy desactualizado. Sigue la [guia de sincronizacion](../git-github/sincronizar-fork.md) o pide ayuda al profesor.

### "No se usar la terminal"

Puedes usar **GitHub Desktop** (programa con interfaz grafica). Descargalo de [desktop.github.com](https://desktop.github.com/).

### "Me equivoque en el nombre de la carpeta"

Renombrala y vuelve a hacer los comandos del Paso 4.

---

## Que NO debes subir

- Archivos de base de datos (`.db`, `.sqlite`)
- Archivos de datos grandes (`.csv` de mas de 1MB)
- Carpetas del sistema (`__pycache__/`, `venv/`, `.venv/`)
- Archivos con contrasenas o tokens

---

## Resumen visual

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUJO DE ENTREGA                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Fork (una vez)                                          │
│     └── Creas tu copia en GitHub                            │
│                                                             │
│  2. Clone (una vez)                                         │
│     └── Descargas la copia a tu PC                          │
│                                                             │
│  3. Trabajas en tu carpeta                                  │
│     └── entregas/.../tu_apellido_nombre/                    │
│                                                             │
│  4. Subes cambios                                           │
│     └── git add . → git commit → git push                   │
│                                                             │
│  5. Pull Request                                            │
│     └── Le dices al profesor "revisame"                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Ayuda

Si tienes dudas:

1. Revisa esta guia de nuevo
2. Pregunta a un companero
3. Pregunta al profesor en clase

---

**Ultima actualizacion:** 2026-02-04
