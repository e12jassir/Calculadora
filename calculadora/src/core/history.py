"""
Sistema de historial con persistencia en JSON.
Almacena y recupera cálculos anteriores.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class CalculationRecord:
    """Registro de un cálculo individual."""
    expression: str
    result: str
    timestamp: str
    mode: str
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'CalculationRecord':
        return cls(**data)


class HistoryManager:
    """
    Gestiona el historial de cálculos con persistencia en archivo JSON.
    Soporta operaciones CRUD básicas.
    """
    
    def __init__(self, file_path: Optional[str] = None):
        """
        Args:
            file_path: Ruta del archivo JSON para persistencia.
                       Si es None, usa ~/.calculadora_history.json
        """
        if file_path is None:
            home = os.path.expanduser('~')
            file_path = os.path.join(home, '.calculadora_history.json')
        
        self.file_path = file_path
        self.records: List[CalculationRecord] = []
        self._load()
    
    def add(self, expression: str, result: str, mode: str = 'deg') -> CalculationRecord:
        """
        Agrega un cálculo al historial.
        
        Args:
            expression: Expresión calculada
            result: Resultado obtenido
            mode: Modo de ángulos ('deg' o 'rad')
        
        Returns:
            El registro creado
        """
        record = CalculationRecord(
            expression=expression,
            result=result,
            timestamp=datetime.now().isoformat(),
            mode=mode
        )
        self.records.append(record)
        self._save()
        return record
    
    def get_all(self) -> List[CalculationRecord]:
        """Retorna todos los registros del historial."""
        return self.records.copy()
    
    def get_last(self, n: int = 10) -> List[CalculationRecord]:
        """Retorna los últimos N registros."""
        return self.records[-n:]
    
    def get_by_index(self, index: int) -> Optional[CalculationRecord]:
        """Retorna un registro por su índice."""
        if 0 <= index < len(self.records):
            return self.records[index]
        return None
    
    def clear(self):
        """Limpia todo el historial."""
        self.records.clear()
        self._save()
    
    def remove(self, index: int) -> bool:
        """
        Elimina un registro por índice.
        
        Returns:
            True si se eliminó, False si el índice no existe
        """
        if 0 <= index < len(self.records):
            self.records.pop(index)
            self._save()
            return True
        return False
    
    def search(self, query: str) -> List[CalculationRecord]:
        """Busca registros que contengan el query."""
        query_lower = query.lower()
        return [
            r for r in self.records
            if query_lower in r.expression.lower() or query_lower in r.result.lower()
        ]
    
    def export_to_text(self, file_path: Optional[str] = None) -> str:
        """Exporta el historial a texto plano."""
        if file_path is None:
            file_path = os.path.expanduser('~/calculadora_export.txt')
        
        lines = []
        lines.append("=" * 60)
        lines.append("HISTORIAL DE CALCULADORA CIENTÍFICA")
        lines.append(f"Exportado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 60)
        lines.append("")
        
        for i, record in enumerate(self.records, 1):
            lines.append(f"[{i}] {record.timestamp}")
            lines.append(f"    {record.expression} = {record.result}")
            lines.append(f"    Modo: {record.mode}")
            lines.append("")
        
        content = '\n'.join(lines)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return content
    
    def _load(self):
        """Carga el historial desde el archivo JSON."""
        if not os.path.exists(self.file_path):
            return
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.records = [
                    CalculationRecord.from_dict(r) for r in data
                ]
        except (json.JSONDecodeError, IOError):
            self.records = []
    
    def _save(self):
        """Guarda el historial en el archivo JSON."""
        try:
            data = [r.to_dict() for r in self.records]
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError:
            pass
    
    def __len__(self) -> int:
        return len(self.records)
    
    def __repr__(self) -> str:
        return f"HistoryManager(records={len(self.records)}, file={self.file_path})"
