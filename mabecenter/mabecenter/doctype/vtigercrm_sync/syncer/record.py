from typing import Dict, Any, Optional, List
import frappe
from frappe import _
from collections import defaultdict, deque

class RecordProcessor:
    def __init__(self, handlers):
        self.handlers = handlers
        self.processing_stack = set()

    def process_record(self, record, fields):
        # Get mapped data from VTiger record
        mapped_data = record.as_dict(fields)
        processed_results = {}

        # Process each entity type in order of dependencies
        processing_order = self._determine_processing_order()

        for entity_type in processing_order:
            if entity_type not in self.handlers:
                continue

            entity_data = mapped_data.get(entity_type, {})

            # Special handling for contacts from owner/spouse/dependents
            if entity_type.lower() == 'contact':
                self._process_contact_entities(entity_data, mapped_data, processed_results)
            else:
                # Normal entity processing
                result = self._create_entity(entity_type, entity_data)
                if result:
                    processed_results[entity_type] = result
                    self._update_dependencies(entity_type, result, processed_results)

        return processed_results

    def _determine_processing_order(self) -> List[str]:
        """
        Determina el orden de procesamiento de las entidades basado en sus dependencias.
        
        :return: Lista ordenada de tipos de entidad.
        :raises: Exception si se detecta una dependencia circular.
        """
        # Construir el grafo de dependencias
        graph = defaultdict(list)  # Nodo -> Lista de nodos dependientes
        indegree = defaultdict(int)  # Nodo -> Número de dependencias entrantes

        # Inicializar nodos y aristas
        for entity, info in self.handlers.items():
            depends_on = info.get('depends_on', [])
            for dependency in depends_on:
                graph[dependency].append(entity)
                indegree[entity] += 1
            if entity not in indegree:
                indegree[entity] = indegree.get(entity, 0)

        # Cola para nodos sin dependencias entrantes
        queue = deque([node for node in indegree if indegree[node] == 0])
        processing_order = []

        while queue:
            current = queue.popleft()
            processing_order.append(current)

            for dependent in graph[current]:
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    queue.append(dependent)

        if len(processing_order) != len(indegree):
            raise Exception("Se detectó una dependencia circular en los handlers.")

        return processing_order

    def _process_contact_entities(self, contact_data, mapped_data, processed_results):
        contact_info = mapped_data.get('Contact', {})

        # Procesar owner como contacto principal
        if 'owner' in contact_info:
            owner_data = contact_info['owner']
            owner_data['is_primary_contact'] = 1
            contact = self._create_entity('contact', owner_data)
            if contact:
                processed_results.setdefault('contacts', []).append(contact)

        # Procesar contacto de spouse
        if 'spouse' in contact_info:
            spouse_data = contact_info['spouse']
            spouse_data['is_primary_contact'] = 0
            contact = self._create_entity('contact', spouse_data)
            if contact:
                processed_results.setdefault('contacts', []).append(contact)

        # Procesar contacto de dependent
        if 'dependent_1' in contact_info:
            dependent_data = contact_info['dependent_1']
            dependent_data['is_primary_contact'] = 0
            contact = self._create_entity('contact', dependent_data)
            if contact:
                processed_results.setdefault('contacts', []).append(contact)

    def _create_entity(self, entity_type: str, data: Dict[str, Any]) -> Optional[Any]:
        """Crea un nuevo documento sin dependencias"""
        if not data:
            return None

        processed_data = self._preprocess_data(data)
        handler_info = self.handlers[entity_type]

        try:
            existing_record = handler_info['handler'].find_existing(processed_data)
            if existing_record:
                return existing_record
            else:
                return handler_info['handler'].process(processed_data)
        except Exception as e:
            frappe.logger().error(f"Error en _create_entity para {entity_type}: {str(e)}")
            raise

    def _update_dependencies(self, entity_type: str, doc: Any, results: Dict[str, Any]):
        """Actualiza el documento con sus dependencias"""
        handler_info = self.handlers[entity_type]

        if not handler_info.get('depends_on'):
            return

        dependencies = {}
        for dependency in handler_info['depends_on']:
            if dependency in results and results[dependency]:
                dependencies[dependency] = results[dependency].name

        if dependencies:
            try:
                handler_info['handler'].update(doc, {}, **dependencies)
            except Exception as e:
                frappe.logger().error(f"Error actualizando dependencias para {entity_type}: {str(e)}")
                raise

    def _resolve_dependencies(self, depends_on: List[str], results: Dict[str, Any], kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resuelve las dependencias para un handler basado en resultados previos y kwargs adicionales.
        
        Args:
            depends_on: Lista de nombres de dependencias
            results: Diccionario con resultados previamente procesados
            kwargs: Argumentos adicionales
            
        Returns:
            Diccionario con dependencias resueltas
        """
        dependencies = {}

        if not depends_on:
            return dependencies

        for dependency in depends_on:
            if dependency in results:
                dependencies[dependency] = results[dependency]
            elif dependency in kwargs:
                dependencies[dependency] = kwargs[dependency]

        return dependencies

    def _preprocess_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Preprocesa los datos de entrada eliminando valores None y cadenas vacías.
        
        Args:
            data: Diccionario con los datos a procesar
            
        Returns:
            Diccionario con datos limpios
        """
        return {
            k: v for k, v in data.items() 
            if v is not None and v != ''
        }