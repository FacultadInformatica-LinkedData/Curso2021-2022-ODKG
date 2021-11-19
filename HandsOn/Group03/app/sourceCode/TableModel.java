
package handson;
import java.util.ArrayList;
import javax.swing.table.*;

public class TableModel extends AbstractTableModel{
    private ArrayList<RecycleBin> bins;
    
    public TableModel(){
        this.bins = new ArrayList<>();
    }

    public int getColumnCount (){
        return 6;
    }

    public int getRowCount(){
        return bins.size();
    }

    @Override
    public String getColumnName(int col){
        String nombre="";

        switch (col){
            case 0: nombre= "District"; break;
            case 1: nombre= "Adress"; break;
            case 2: nombre="Waste Type"; break;
            case 3: nombre="Capacity"; break;
            case 4: nombre="State"; break;
            case 5: nombre = "Last Update"; break;
        }
        return nombre;
    }

    @Override
    public Class getColumnClass(int col){
        Class clase=null;

        switch (col){
            case 0: clase= java.lang.String.class; break;
            case 1: clase= java.lang.String.class; break;
            case 2: clase=java.lang.String.class; break;
            case 3: clase= java.lang.String.class; break;
            case 4: clase=java.lang.String.class; break;
            case 5: clase=java.lang.String.class; break;
        }
        return clase;
    }

    @Override
    public boolean isCellEditable(int row, int col){
        return false;
    }

    public Object getValueAt(int row, int col){
        Object resultado=null;
        switch (col){
            case 0: resultado= bins.get(row).getDistrict(); break;
            case 1: resultado= bins.get(row).getAdress(); break;
            case 2: resultado=bins.get(row).getWasteType();break;
            case 3: resultado=bins.get(row).getCapacity();break;
            case 4: resultado=bins.get(row).getState();break;
            case 5: resultado=bins.get(row).getLastUpdate();break;
        }
        return resultado;
    }

    public void setRows(ArrayList<RecycleBin> bins){
        this.bins=bins;
        fireTableDataChanged();
    }

    public RecycleBin getBin(int i){
        return this.bins.get(i);
    }

}
