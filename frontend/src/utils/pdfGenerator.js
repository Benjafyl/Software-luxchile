import { jsPDF } from 'jspdf';
import autoTable from 'jspdf-autotable';

/**
 * Genera PDF de Asignaciones de Carga
 */
export const generateAsignacionesPDF = (asignaciones) => {
  const doc = new jsPDF();
  
  // Título
  doc.setFontSize(18);
  doc.setFont(undefined, 'bold');
  doc.text('Reporte de Asignaciones de Carga', 14, 20);
  
  // Fecha de generación
  doc.setFontSize(10);
  doc.setFont(undefined, 'normal');
  const fecha = new Date().toLocaleString('es-CL');
  doc.text(`Fecha de generación: ${fecha}`, 14, 28);
  
  // Preparar datos para la tabla
  const tableData = asignaciones.map(asig => [
    asig.cargo_id || '-',
    asig.vehicle_id || '-',
    asig.prioridad || '-',
    asig.origen || '-',
    asig.destino || '-',
    asig.responsable?.nombre || asig.responsable?.rut || '-',
    asig.fecha_hora ? new Date(asig.fecha_hora).toLocaleString('es-CL') : '-'
  ]);
  
  // Generar tabla usando autoTable
  autoTable(doc, {
    head: [['Cargo ID', 'Vehículo', 'Prioridad', 'Origen', 'Destino', 'Responsable', 'Fecha/Hora']],
    body: tableData,
    startY: 35,
    styles: { fontSize: 8, cellPadding: 2 },
    headStyles: { fillColor: [41, 128, 185], textColor: 255, fontStyle: 'bold' },
    alternateRowStyles: { fillColor: [245, 245, 245] },
    margin: { top: 35 },
    didDrawPage: function (data) {
      // Footer con número de página
      const pageCount = doc.internal.getNumberOfPages();
      doc.setFontSize(8);
      doc.text(
        `Página ${data.pageNumber} de ${pageCount}`,
        doc.internal.pageSize.getWidth() / 2,
        doc.internal.pageSize.getHeight() - 10,
        { align: 'center' }
      );
    }
  });
  
  // Resumen
  const finalY = doc.lastAutoTable.finalY + 10;
  doc.setFontSize(10);
  doc.setFont(undefined, 'bold');
  doc.text(`Total de asignaciones: ${asignaciones.length}`, 14, finalY);
  
  // Guardar PDF
  doc.save(`asignaciones_${new Date().getTime()}.pdf`);
};

/**
 * Genera PDF de Incidentes
 */
export const generateIncidentesPDF = (incidentes) => {
  const doc = new jsPDF();
  
  // Título
  doc.setFontSize(18);
  doc.setFont(undefined, 'bold');
  doc.text('Reporte de Incidentes', 14, 20);
  
  // Fecha de generación
  doc.setFontSize(10);
  doc.setFont(undefined, 'normal');
  const fecha = new Date().toLocaleString('es-CL');
  doc.text(`Fecha de generación: ${fecha}`, 14, 28);
  
  // Preparar datos para la tabla
  const tableData = incidentes.map(inc => [
    inc.cargo_id || '-',
    inc.vehicle_id || '-',
    inc.employee_id || '-',
    inc.type || '-',
    inc.description ? (inc.description.length > 40 ? inc.description.substring(0, 37) + '...' : inc.description) : '-',
    inc.created_at ? new Date(inc.created_at).toLocaleString('es-CL') : '-'
  ]);
  
  // Generar tabla usando autoTable
  autoTable(doc, {
    head: [['Cargo ID', 'Vehículo', 'RUT Empleado', 'Tipo', 'Descripción', 'Fecha/Hora']],
    body: tableData,
    startY: 35,
    styles: { fontSize: 8, cellPadding: 2 },
    headStyles: { fillColor: [231, 76, 60], textColor: 255, fontStyle: 'bold' },
    alternateRowStyles: { fillColor: [245, 245, 245] },
    margin: { top: 35 },
    didDrawPage: function (data) {
      // Footer con número de página
      const pageCount = doc.internal.getNumberOfPages();
      doc.setFontSize(8);
      doc.text(
        `Página ${data.pageNumber} de ${pageCount}`,
        doc.internal.pageSize.getWidth() / 2,
        doc.internal.pageSize.getHeight() - 10,
        { align: 'center' }
      );
    }
  });
  
  // Resumen por tipo
  const finalY = doc.lastAutoTable.finalY + 10;
  doc.setFontSize(10);
  doc.setFont(undefined, 'bold');
  doc.text(`Total de incidentes: ${incidentes.length}`, 14, finalY);
  
  // Contar por tipo
  const tiposCounts = incidentes.reduce((acc, inc) => {
    acc[inc.type] = (acc[inc.type] || 0) + 1;
    return acc;
  }, {});
  
  let yPos = finalY + 6;
  doc.setFontSize(9);
  doc.setFont(undefined, 'normal');
  Object.entries(tiposCounts).forEach(([tipo, count]) => {
    doc.text(`  • ${tipo}: ${count}`, 14, yPos);
    yPos += 5;
  });
  
  // Guardar PDF
  doc.save(`incidentes_${new Date().getTime()}.pdf`);
};
