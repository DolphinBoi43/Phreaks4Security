<mxfile host="app.diagrams.net" modified="2025-11-08T00:00:00.000Z" agent="draw.io" version="28.2.7">
  <diagram id="HW" name="Hardware">
    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="900" math="0" shadow="0">
      <root>
        <mxCell id="0"/><mxCell id="1" parent="0"/>
        <!-- Power -->
        <mxCell id="pwr_ac" value="AC 120 V" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;" vertex="1" parent="1"><mxGeometry x="60" y="70" width="120" height="40" as="geometry"/></mxCell>
        <mxCell id="pwr_5v" value="5 V DC Supply" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;" vertex="1" parent="1"><mxGeometry x="220" y="70" width="140" height="40" as="geometry"/></mxCell>
        <mxCell id="edge_ac_psu" style="edgeStyle=orthogonalEdgeStyle;html=1;strokeColor=#d79b00;" edge="1" parent="1" source="pwr_ac" target="pwr_5v"><mxGeometry relative="1" as="geometry"/></mxCell>

        <!-- RPI and STM32 -->
        <mxCell id="pi" value="Raspberry Pi 3B+" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e51400;fontColor=#ffffff;strokeColor=#B20000;" vertex="1" parent="1"><mxGeometry x="220" y="180" width="180" height="80" as="geometry"/></mxCell>
        <mxCell id="stm" value="STM32 Nucleo" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#1ba1e2;fontColor=#ffffff;strokeColor=#006EAF;" vertex="1" parent="1"><mxGeometry x="60" y="180" width="160" height="80" as="geometry"/></mxCell>

        <!-- 5V to boards -->
        <mxCell id="edge_psu_stm" style="edgeStyle=orthogonalEdgeStyle;html=1;strokeColor=#d79b00;" edge="1" parent="1" source="pwr_5v" target="stm"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="edge_psu_pi" style="edgeStyle=orthogonalEdgeStyle;html=1;strokeColor=#d79b00;" edge="1" parent="1" source="pwr_5v" target="pi"><mxGeometry relative="1" as="geometry"/></mxCell>

        <!-- Sensors to STM32 -->
        <mxCell id="pir" value="PIR Motion" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1"><mxGeometry x="60" y="300" width="120" height="50" as="geometry"/></mxCell>
        <mxCell id="reed" value="Door/Window Reed" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1"><mxGeometry x="60" y="360" width="160" height="50" as="geometry"/></mxCell>
        <mxCell id="edge_pir_stm" style="edgeStyle=orthogonalEdgeStyle;html=1;" edge="1" parent="1" source="pir" target="stm"><mxGeometry relative="1" as="geometry"><mxPoint x="140" y="220" as="targetPoint"/></mxGeometry></mxCell>
        <mxCell id="edge_reed_stm" style="edgeStyle=orthogonalEdgeStyle;html=1;" edge="1" parent="1" source="reed" target="stm"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="label_gpio" value="GPIO" style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;labelBackgroundColor=#ffffff;" vertex="1" connectable="0" parent="edge_pir_stm"><mxGeometry x="-0.2" y="-1" relative="1" as="geometry"><mxPoint x="0" y="-10" as="offset"/></mxGeometry></mxCell>

        <!-- UART one-way STM32 -> Pi -->
        <mxCell id="edge_uart" style="edgeStyle=orthogonalEdgeStyle;html=1;endArrow=classic;endFill=1;strokeColor=#006EAF;" edge="1" parent="1" source="stm" target="pi"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="uart_label" value="UART 115200 8N1 (ASCII lines &#10;MOTION / DOOR_OPEN / HEARTBEAT)" style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;labelBackgroundColor=#ffffff;" vertex="1" connectable="0" parent="edge_uart"><mxGeometry x="0.1" y="-1" relative="1" as="geometry"><mxPoint x="0" y="-10" as="offset"/></mxGeometry></mxCell>

        <!-- Pi peripherals -->
        <mxCell id="cam" value="Pi Camera (CSI)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1"><mxGeometry x="430" y="170" width="150" height="40" as="geometry"/></mxCell>
        <mxCell id="mic" value="USB Microphone" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1"><mxGeometry x="430" y="220" width="150" height="40" as="geometry"/></mxCell>
        <mxCell id="buzz" value="Buzzer / Speaker (Audio Out)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1"><mxGeometry x="430" y="270" width="200" height="40" as="geometry"/></mxCell>
        <mxCell id="edge_cam_pi" style="edgeStyle=orthogonalEdgeStyle;html=1;" edge="1" parent="1" source="cam" target="pi"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="edge_mic_pi" style="edgeStyle=orthogonalEdgeStyle;html=1;" edge="1" parent="1" source="mic" target="pi"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="edge_buzz_pi" style="edgeStyle=orthogonalEdgeStyle;html=1;" edge="1" parent="1" source="buzz" target="pi"><mxGeometry relative="1" as="geometry"/></mxCell>

        <!-- Network -->
        <mxCell id="viewer" value="Viewer (Phone/PC on LAN)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1"><mxGeometry x="430" y="330" width="200" height="40" as="geometry"/></mxCell>
        <mxCell id="edge_wifi" style="edgeStyle=orthogonalEdgeStyle;html=1;dashed=1;strokeColor=#82b366;" edge="1" parent="1" source="pi" target="viewer"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="wifi_label" value="Wi-Fi (LAN): /last.jpg, /health" style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;labelBackgroundColor=#ffffff;" vertex="1" connectable="0" parent="edge_wifi"><mxGeometry x="0.05" y="-1" relative="1" as="geometry"><mxPoint x="0" y="-10" as="offset"/></mxGeometry></mxCell>
      </root>
    </mxGraphModel>
  </diagram>

  <diagram id="SW" name="Software">
    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="900" math="0" shadow="0">
      <root>
        <mxCell id="0"/><mxCell id="1" parent="0"/>

        <!-- STM32 firmware group -->
        <mxCell id="fw_group" value="STM32 Firmware" style="swimlane;rounded=0;childLayout=stackLayout;horizontal=1;startSize=28;fillColor=#cfe2f3;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="60" y="140" width="380" height="280" as="geometry"/>
        </mxCell>
        <mxCell id="fw_sens" value="Sensor Drivers (PIR, Reed)" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#6c8ebf;fillColor=#ffffff;" vertex="1" parent="fw_group"><mxGeometry x="30" y="40" width="320" height="60" as="geometry"/></mxCell>
        <mxCell id="fw_deb" value="Debounce &amp; State Machine" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#6c8ebf;fillColor=#ffffff;" vertex="1" parent="fw_group"><mxGeometry x="30" y="110" width="320" height="60" as="geometry"/></mxCell>
        <mxCell id="fw_enc" value="Event Encoder (MOTION, DOOR_OPEN, DOOR_CLOSED, HEARTBEAT)" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#6c8ebf;fillColor=#ffffff;" vertex="1" parent="fw_group"><mxGeometry x="30" y="180" width="320" height="60" as="geometry"/></mxCell>
        <mxCell id="fw_uart" value="UART TX @115200 8N1 (ASCII + '\n')" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#6c8ebf;fillColor=#ffffff;" vertex="1" parent="fw_group"><mxGeometry x="30" y="250" width="320" height="60" as="geometry"/></mxCell>

        <!-- Pi daemon group -->
        <mxCell id="pi_group" value="Raspberry Pi (systemd Python Daemon)" style="swimlane;rounded=0;childLayout=stackLayout;horizontal=1;startSize=28;fillColor=#f4cccc;strokeColor=#cc0000;" vertex="1" parent="1">
          <mxGeometry x="540" y="120" width="500" height="340" as="geometry"/>
        </mxCell>
        <mxCell id="pi_rx" value="UART Listener" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#cc0000;fillColor=#ffffff;" vertex="1" parent="pi_group"><mxGeometry x="30" y="40" width="440" height="50" as="geometry"/></mxCell>
        <mxCell id="pi_router" value="Event Router" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#cc0000;fillColor=#ffffff;" vertex="1" parent="pi_group"><mxGeometry x="30" y="100" width="440" height="50" as="geometry"/></mxCell>
        <mxCell id="pi_cap" value="Capture Snapshot (OpenCV)" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#cc0000;fillColor=#ffffff;" vertex="1" parent="pi_group"><mxGeometry x="30" y="160" width="440" height="50" as="geometry"/></mxCell>
        <mxCell id="pi_aud" value="Play Alert (aplay)" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#cc0000;fillColor=#ffffff;" vertex="1" parent="pi_group"><mxGeometry x="30" y="220" width="440" height="50" as="geometry"/></mxCell>
        <mxCell id="pi_log" value="Append CSV Log (events.csv)" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#cc0000;fillColor=#ffffff;" vertex="1" parent="pi_group"><mxGeometry x="30" y="280" width="440" height="50" as="geometry"/></mxCell>

        <!-- Optional micro-API -->
        <mxCell id="api_group" value="Flask Mini-API" style="swimlane;rounded=0;childLayout=stackLayout;horizontal=1;startSize=28;fillColor=#d9ead3;strokeColor=#6aa84f;" vertex="1" parent="1">
          <mxGeometry x="540" y="480" width="500" height="130" as="geometry"/>
        </mxCell>
        <mxCell id="api_last" value="GET /last.jpg → last snapshot" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#6aa84f;fillColor=#ffffff;" vertex="1" parent="api_group"><mxGeometry x="30" y="40" width="440" height="40" as="geometry"/></mxCell>
        <mxCell id="api_health" value="GET /health → { ok, last_image }" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#6aa84f;fillColor=#ffffff;" vertex="1" parent="api_group"><mxGeometry x="30" y="85" width="440" height="40" as="geometry"/></mxCell>

        <!-- Connections -->
        <mxCell id="edge_fw_pi" style="edgeStyle=orthogonalEdgeStyle;html=1;endArrow=classic;endFill=1;strokeColor=#006EAF;" edge="1" parent="1" source="fw_uart" target="pi_rx"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="edge_rx_router" style="edgeStyle=orthogonalEdgeStyle;html=1;" edge="1" parent="1" source="pi_rx" target="pi_router"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="edge_router_cap" style="edgeStyle=orthogonalEdgeStyle;html=1;" edge="1" parent="1" source="pi_router" target="pi_cap"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="edge_router_aud" style="edgeStyle=orthogonalEdgeStyle;html=1;" edge="1" parent="1" source="pi_router" target="pi_aud"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="edge_router_log" style="edgeStyle=orthogonalEdgeStyle;html=1;" edge="1" parent="1" source="pi_router" target="pi_log"><mxGeometry relative="1" as="geometry"/></mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
