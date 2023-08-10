within ThermoSysPro.InstrumentationAndControl.Blocks.Math;
block Div

  ThermoSysPro.InstrumentationAndControl.Connectors.InputReal u1
                                       annotation (Placement(transformation(
          extent={{-120,50},{-100,70}}, rotation=0)));
  ThermoSysPro.InstrumentationAndControl.Connectors.InputReal u2
                                       annotation (Placement(transformation(
          extent={{-120,-70},{-100,-50}}, rotation=0)));
  ThermoSysPro.InstrumentationAndControl.Connectors.OutputReal y
                                       annotation (Placement(transformation(
          extent={{100,-10},{120,10}}, rotation=0)));
equation

  y.signal = u1.signal/u2.signal;
  annotation (
    Icon(coordinateSystem(
        preserveAspectRatio=false,
        extent={{-100,-100},{100,100}},
        grid={2,2}), graphics={
        Line(points={{50,0},{100,0}}),
        Line(points={{50,0},{100,0}}),
        Rectangle(
          extent={{-100,-100},{100,100}},
          lineColor={0,0,255},
          fillColor={255,255,255},
          fillPattern=FillPattern.Solid),
        Text(extent={{-150,150},{150,110}}, textString=
                                                "%name"),
        Line(points={{80,0},{100,0}}),
        Line(points={{80,0},{100,0}}),
        Ellipse(extent={{-80,80},{80,-80}}),
        Line(points={{80,0},{100,0}}),
        Line(points={{-100,60},{-52,60}}),
        Line(points={{-100,-60},{-52,-60}}),
        Text(
          extent={{-36,34},{40,-34}},
          lineColor={0,0,0},
          textString=
               "/")}),
    Diagram(coordinateSystem(
        preserveAspectRatio=false,
        extent={{-100,-100},{100,100}},
        grid={2,2}), graphics={
        Line(points={{50,0},{100,0}}),
        Line(points={{50,0},{100,0}}),
        Rectangle(
          extent={{-100,-100},{100,100}},
          lineColor={0,0,255},
          fillColor={255,255,255},
          fillPattern=FillPattern.Solid),
        Line(points={{80,0},{100,0}}),
        Line(points={{80,0},{100,0}}),
        Ellipse(extent={{-80,80},{80,-80}}),
        Line(points={{80,0},{100,0}}),
        Line(points={{-100,60},{-52,60}}),
        Line(points={{-100,-60},{-52,-60}}),
        Text(
          extent={{-36,34},{40,-34}},
          lineColor={0,0,0},
          textString=
               "/")}),
    Window(
      x=0.31,
      y=0.18,
      width=0.6,
      height=0.6),
    Documentation(info="<html>
<p><b>Adapted from the Modelica.Blocks.Math library</b></p>
</HTML>
<html>
<p><b>Version 1.0</b></p>
</HTML>
"));
end Div;
