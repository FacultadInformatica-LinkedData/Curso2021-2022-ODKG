package handson;

import java.time.LocalDateTime;


public class RecycleBin {
    private String capacity;
    private String adress;
    private String district;
    private String wasteType;
    private String state;
    private String lastUpdate;

    public RecycleBin(String capacity, String adress, String district, String wasteType, String state, String lastUpdate) {
        this.capacity = capacity;
        this.adress = adress;
        this.district = district;
        this.wasteType = wasteType;
        this.state = state;
        this.lastUpdate = lastUpdate;
    }

    public String getCapacity() {
        return capacity;
    }

    public void setCapacity(String capacity) {
        this.capacity = capacity;
    }

    public String getAdress() {
        return adress;
    }

    public void setAdress(String adress) {
        this.adress = adress;
    }

    public String getDistrict() {
        return district;
    }

    public void setDistrict(String district) {
        this.district = district;
    }

    public String getWasteType() {
        return wasteType;
    }

    public void setWasteType(String wasteType) {
        this.wasteType = wasteType;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public String getLastUpdate() {
        return lastUpdate;
    }

    public void setLastUpdate(String lastUpdate) {
        this.lastUpdate = lastUpdate;
    }
    
    
}
