/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package handson;

import java.util.ArrayList;

/**
 *
 * @author miguel
 */
public class GUI extends javax.swing.JFrame {

    private ResultsGUI results;
    private QueryHandler query;
    
    public GUI() {
        initComponents();
        this.query = new QueryHandler();
        results = null;
    }

    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        exitButton = new javax.swing.JButton();
        queryButton = new javax.swing.JButton();
        capacityBox = new javax.swing.JComboBox<>();
        districtBox = new javax.swing.JComboBox<>();
        stateBox = new javax.swing.JComboBox<>();
        jLabel1 = new javax.swing.JLabel();
        jLabel2 = new javax.swing.JLabel();
        jLabel3 = new javax.swing.JLabel();
        jLabel6 = new javax.swing.JLabel();
        wasteBox = new javax.swing.JComboBox<>();
        jLabel4 = new javax.swing.JLabel();
        jLabel7 = new javax.swing.JLabel();
        jLabel8 = new javax.swing.JLabel();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        getContentPane().setLayout(new org.netbeans.lib.awtextra.AbsoluteLayout());

        exitButton.setBackground(new java.awt.Color(255, 0, 0));
        exitButton.setText("EXIT");
        exitButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                exitButtonActionPerformed(evt);
            }
        });
        getContentPane().add(exitButton, new org.netbeans.lib.awtextra.AbsoluteConstraints(0, 360, 170, 57));

        queryButton.setBackground(new java.awt.Color(0, 255, 0));
        queryButton.setText("Run Query");
        queryButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                queryButtonActionPerformed(evt);
            }
        });
        getContentPane().add(queryButton, new org.netbeans.lib.awtextra.AbsoluteConstraints(710, 360, 175, 57));

        capacityBox.setModel(new javax.swing.DefaultComboBoxModel<>(new String[] { "Any", "0", "2", "4", "6", "8", "10" }));
        capacityBox.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                capacityBoxActionPerformed(evt);
            }
        });
        getContentPane().add(capacityBox, new org.netbeans.lib.awtextra.AbsoluteConstraints(450, 210, 181, 20));

        districtBox.setModel(new javax.swing.DefaultComboBoxModel<>(new String[] { "Any", "Arganzuela", "Barajas", "Carabanchel", "Centro", "Chamberí", "Chamartín", "Ciudad Lineal", "Fuencarral-El Pardo", "Hortaleza", "Latina", "Moncloa-Aravaca", "Moratalaz", "Puente de Vallecas", "Retiro", "Salamanca", "San Blas", "Tetuán", "Usera", "Vicálvaro", "Villaverde", "Villa de Vallecas" }));
        districtBox.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                districtBoxActionPerformed(evt);
            }
        });
        getContentPane().add(districtBox, new org.netbeans.lib.awtextra.AbsoluteConstraints(250, 210, 181, 20));

        stateBox.setModel(new javax.swing.DefaultComboBoxModel<>(new String[] { "Any", "OK", "FULL", "ERROR" }));
        stateBox.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                stateBoxActionPerformed(evt);
            }
        });
        getContentPane().add(stateBox, new org.netbeans.lib.awtextra.AbsoluteConstraints(450, 300, 181, -1));

        jLabel1.setText("Capacity");
        getContentPane().add(jLabel1, new org.netbeans.lib.awtextra.AbsoluteConstraints(510, 170, -1, 10));

        jLabel2.setText("District");
        getContentPane().add(jLabel2, new org.netbeans.lib.awtextra.AbsoluteConstraints(310, 170, -1, 10));

        jLabel3.setText("State");
        getContentPane().add(jLabel3, new org.netbeans.lib.awtextra.AbsoluteConstraints(520, 270, -1, -1));

        jLabel6.setText("Waste Type");
        getContentPane().add(jLabel6, new org.netbeans.lib.awtextra.AbsoluteConstraints(300, 270, -1, -1));

        wasteBox.setModel(new javax.swing.DefaultComboBoxModel<>(new String[] { "Any", "Plastic", "Organic" }));
        wasteBox.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                wasteBoxActionPerformed(evt);
            }
        });
        getContentPane().add(wasteBox, new org.netbeans.lib.awtextra.AbsoluteConstraints(250, 300, 181, -1));

        jLabel4.setFont(new java.awt.Font("Dialog", 1, 24)); // NOI18N
        jLabel4.setText("SMART RECYCLE BINS");
        getContentPane().add(jLabel4, new org.netbeans.lib.awtextra.AbsoluteConstraints(300, 30, -1, -1));

        jLabel7.setText("This App provides an interface that facilitates tools to search and filter Madrid's Smart Recycle Bin System");
        getContentPane().add(jLabel7, new org.netbeans.lib.awtextra.AbsoluteConstraints(70, 100, -1, -1));

        jLabel8.setText("Each bin contains information about its state, waste type and location.");
        getContentPane().add(jLabel8, new org.netbeans.lib.awtextra.AbsoluteConstraints(180, 120, -1, -1));

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void exitButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_exitButtonActionPerformed
        System.exit(0);
    }//GEN-LAST:event_exitButtonActionPerformed

    private void queryButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_queryButtonActionPerformed
        ArrayList<RecycleBin> result = new ArrayList<>();
        QueryHandler q = new QueryHandler();
        
        String c = capacityBox.getSelectedItem().toString();
        if(c.equals("Any")) c = "-1";
        Integer capacity = Integer.valueOf(c);
        
        String w = wasteBox.getSelectedItem().toString();
        String wdef = "";
        if(w.equals("Plastic")) wdef = "envases";
        else if (w.equals("Organic")) wdef = "resto";
        else wdef = "Any";
        
        result = q.query(districtBox.getSelectedItem().toString(), capacity, 
                wdef, stateBox.getSelectedItem().toString());
        if(results == null){
            results = new ResultsGUI();
        }
        results.setBins(result);
        results.setVisible(true);
    }//GEN-LAST:event_queryButtonActionPerformed

    private void capacityBoxActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_capacityBoxActionPerformed
        // TODO add your handling code here:
    }//GEN-LAST:event_capacityBoxActionPerformed

    private void districtBoxActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_districtBoxActionPerformed
        // TODO add your handling code here:
    }//GEN-LAST:event_districtBoxActionPerformed

    private void stateBoxActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_stateBoxActionPerformed
        // TODO add your handling code here:
    }//GEN-LAST:event_stateBoxActionPerformed

    private void wasteBoxActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_wasteBoxActionPerformed
        // TODO add your handling code here:
    }//GEN-LAST:event_wasteBoxActionPerformed


    public static void main(String args[]) {

        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                GUI a = new GUI();
                a.setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JComboBox<String> capacityBox;
    private javax.swing.JComboBox<String> districtBox;
    private javax.swing.JButton exitButton;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JLabel jLabel3;
    private javax.swing.JLabel jLabel4;
    private javax.swing.JLabel jLabel6;
    private javax.swing.JLabel jLabel7;
    private javax.swing.JLabel jLabel8;
    private javax.swing.JButton queryButton;
    private javax.swing.JComboBox<String> stateBox;
    private javax.swing.JComboBox<String> wasteBox;
    // End of variables declaration//GEN-END:variables
}
