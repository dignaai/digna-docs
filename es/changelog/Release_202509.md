# Registro de cambios – Versión 2025.09  

Con la Versión 2025.09, digna introduce una nueva **arquitectura modular** y lanza **cinco módulos especializados** para Calidad de Datos y Observabilidad.  
Esta versión también refuerza la autenticación y mejora la gestión de notificaciones en toda la plataforma.  

---

## Nuevas funciones  

### Diseño modular  
- digna ahora sigue una **arquitectura modular**.  
- Los clientes pueden habilitar solo los módulos que necesiten y añadir más según crezcan sus requisitos.  
- La funcionalidad anterior ahora forma parte de **digna Data Anomalies**.  

### Nuevos módulos  
- **digna Data Anomalies** – Detección con IA de anomalías en volúmenes de datos, distribuciones y valores faltantes.  
- **digna Data Analytics** – Evaluación en series temporales de métricas de observabilidad para detectar tendencias y volatilidad a largo plazo.  
- **digna Data Timeliness** – Monitorización de los tiempos esperados de llegada de datos, tanto basada en IA como en reglas.  
- **digna Data Validation** – Comprobaciones a nivel de registro basadas en reglas para asegurar el cumplimiento de las normas de negocio.  
- **digna Data Schema Tracker** – Detección de cambios de esquema (modificaciones DDL) en bases de datos monitorizadas.  

### MFA vía OIDC  
- Soporte para Autenticación Multifactor (MFA) con OIDC Single Sign-On.  
- Ofrece seguridad de nivel empresarial para todos los inicios de sesión de usuarios.  

### Correos de notificación por módulo  
- Las notificaciones ahora se envían **por módulo**, facilitando separar las alertas de Data Anomalies, Data Analytics y otros módulos.  

---

## Actualizaciones de la CLI  

- **Nuevo comando: `inspect-cancel`** – Cancelar inspecciones por ID de solicitud o terminar todas las solicitudes activas.  
- **Nuevo comando: `check-config`** – Validar archivos de configuración antes del arranque.  
- **Nuevo comando: `remove-orphans`** – Limpiar entradas huérfanas del repositorio.  
- **Comando `inspect` mejorado** – Nueva opción `--bypass-backend` (`-bb`) y códigos de retorno estandarizados (`0 = OK, 1 = INFO, 2 = WARNING`).  


## Documentación  
- Nuevas guías:  
  - Guía de integración de Single Sign-On