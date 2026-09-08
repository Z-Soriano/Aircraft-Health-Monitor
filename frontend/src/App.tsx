import "./App.css";

type Telemetry = {
  sequenceNumber: number;
  timestamp: string;
  altitude: number;
  speed: number;
  battery: number;
  temperature: number;
  status: "NORMAL" | "WARNING";
  warnings: string[];
};

type MetricCardProps = {
  label: string;
  value: string;
  unit: string;
  accent: "blue" | "green" | "orange" | "purple";
};

type NumericTelemetryKey =
  | "altitude"
  | "speed"
  | "battery"
  | "temperature";

type LineChartProps = {
  title: string;
  unit: string;
  color: string;
  dataKey: NumericTelemetryKey;
  telemetryHistory: Telemetry[];
};

const mockTelemetry: Telemetry = {
  sequenceNumber: 42,
  timestamp: "2026-09-08T03:20:04+00:00",
  altitude: 5012.7,
  speed: 119.4,
  battery: 87.8,
  temperature: 75.3,
  status: "NORMAL",
  warnings: [],
};

const mockHistoryValues = [
  { altitude: 4985.2, speed: 117.2, battery: 89.1, temperature: 73.8 },
  { altitude: 4991.7, speed: 117.9, battery: 89.0, temperature: 74.1 },
  { altitude: 4998.4, speed: 118.5, battery: 88.9, temperature: 74.4 },
  { altitude: 5006.1, speed: 119.1, battery: 88.7, temperature: 74.8 },
  { altitude: 5014.8, speed: 120.2, battery: 88.6, temperature: 75.1 },
  { altitude: 5009.3, speed: 119.8, battery: 88.4, temperature: 75.5 },
  { altitude: 5018.9, speed: 120.6, battery: 88.3, temperature: 75.8 },
  { altitude: 5024.2, speed: 121.1, battery: 88.1, temperature: 76.0 },
  { altitude: 5017.5, speed: 120.4, battery: 88.0, temperature: 75.7 },
  { altitude: 5008.6, speed: 119.9, battery: 87.9, temperature: 75.5 },
  { altitude: 5012.7, speed: 119.4, battery: 87.8, temperature: 75.3 },
];

const mockTelemetryHistory: Telemetry[] = mockHistoryValues.map(
  (values, index) => ({
    sequenceNumber: 32 + index,
    timestamp: new Date(
      Date.parse("2026-09-08T03:19:54+00:00") + index * 1000,
    ).toISOString(),
    ...values,
    status: "NORMAL",
    warnings: [],
  }),
);



function MetricCard({
  label,
  value,
  unit,
  accent,
}: MetricCardProps) {
  return (
    <article className={`metricCard ${accent}`}>
      <p className="metricLabel">{label}</p>

      <div className="metricReading">
        <span className="metricValue">{value}</span>
        <span className="metricUnit">{unit}</span>
      </div>
    </article>
  );
}

function LineChart({
  title,
  unit,
  color,
  dataKey,
  telemetryHistory,
}: LineChartProps) {
  const width = 560;
  const height = 230;

  const padding = {
    top: 20,
    right: 20,
    bottom: 38,
    left: 58,
  };

  const plotWidth = width - padding.left - padding.right;
  const plotHeight = height - padding.top - padding.bottom;

  const values = telemetryHistory.map(
    (reading) => reading[dataKey],
  );

  const rawMinimum = Math.min(...values);
  const rawMaximum = Math.max(...values);
  const valueRange = rawMaximum - rawMinimum || 1;

  const minimumValue = rawMinimum - valueRange * 0.15;
  const maximumValue = rawMaximum + valueRange * 0.15;

  function getXPosition(index: number) {
    if (telemetryHistory.length === 1) {
      return padding.left + plotWidth / 2;
    }

    return (
      padding.left +
      (index / (telemetryHistory.length - 1)) * plotWidth
    );
  }

  function getYPosition(value: number) {
    return (
      padding.top +
      ((maximumValue - value) /
        (maximumValue - minimumValue)) *
        plotHeight
    );
  }

  const linePoints = values
    .map(
      (value, index) =>
        `${getXPosition(index)},${getYPosition(value)}`,
    )
    .join(" ");

  const chartBottom = height - padding.bottom;

  const areaPoints = [
    `${padding.left},${chartBottom}`,
    linePoints,
    `${width - padding.right},${chartBottom}`,
  ].join(" ");

  const currentValue = values[values.length - 1];
  const firstSequence = telemetryHistory[0].sequenceNumber;
  const lastSequence =
    telemetryHistory[telemetryHistory.length - 1].sequenceNumber;

  const gridPositions = [0, 0.5, 1];

  return (
    <article className="chartCard">
      <div className="chartHeader">
        <div>
          <p className="chartTitle">{title}</p>
          <p className="chartSubtitle">
            Last {telemetryHistory.length} readings
          </p>
        </div>

        <div className="chartCurrentValue">
          {currentValue.toFixed(1)}
          <span>{unit}</span>
        </div>
      </div>

      <svg
        className="lineChart"
        viewBox={`0 0 ${width} ${height}`}
        role="img"
        aria-label={`${title} over recent telemetry readings`}
      >
        {gridPositions.map((position) => {
          const yPosition =
            padding.top + position * plotHeight;

          const labelValue =
            maximumValue -
            position * (maximumValue - minimumValue);

          return (
            <g key={position}>
              <line
                className="chartGridLine"
                x1={padding.left}
                x2={width - padding.right}
                y1={yPosition}
                y2={yPosition}
              />

              <text
                className="chartAxisLabel"
                x={padding.left - 10}
                y={yPosition + 4}
                textAnchor="end"
              >
                {labelValue.toFixed(1)}
              </text>
            </g>
          );
        })}

        <polygon
          points={areaPoints}
          fill={color}
          opacity="0.08"
        />

        <polyline
          points={linePoints}
          fill="none"
          stroke={color}
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        <circle
          cx={getXPosition(values.length - 1)}
          cy={getYPosition(currentValue)}
          r="5"
          fill={color}
        />

        <text
          className="chartAxisLabel"
          x={padding.left}
          y={height - 10}
          textAnchor="start"
        >
          #{firstSequence}
        </text>

        <text
          className="chartAxisLabel"
          x={width - padding.right}
          y={height - 10}
          textAnchor="end"
        >
          #{lastSequence}
        </text>

        <text
          className="chartAxisTitle"
          x={width / 2}
          y={height - 10}
          textAnchor="middle"
        >
          Telemetry sequence
        </text>
      </svg>
    </article>
  );
}

function App() {
  const telemetry = mockTelemetry;
  const hasWarnings = telemetry.warnings.length > 0;

  const formattedTime = new Date(telemetry.timestamp).toLocaleTimeString();

  return (
    <main className="dashboardShell">
      <header className="appHeader">
        <div>
          <p className="eyebrow">GROUND CONTROL</p>
          <h1>Aircraft Telemetry</h1>
          <p className="subtitle">
            Live flight data and aircraft health monitoring
          </p>
        </div>

        <div className="connectionStatus">
          <span className="connectionDot" />
          Connected
        </div>
      </header>

      <section className="flightBar">
        <div>
          <span className="flightLabel">Flight</span>
          <strong>SIM-001</strong>
        </div>

        <div>
          <span className="flightLabel">Sequence</span>
          <strong>#{telemetry.sequenceNumber}</strong>
        </div>

        <div>
          <span className="flightLabel">Last update</span>
          <strong>{formattedTime}</strong>
        </div>

        <div>
          <span className="flightLabel">Overall status</span>
          <strong
            className={
              telemetry.status === "NORMAL"
                ? "normalText"
                : "warningText"
            }
          >
            {telemetry.status}
          </strong>
        </div>
      </section>

      <section className="metricGrid">
        <MetricCard
          label="Altitude"
          value={telemetry.altitude.toFixed(1)}
          unit="ft"
          accent="blue"
        />

        <MetricCard
          label="Airspeed"
          value={telemetry.speed.toFixed(1)}
          unit="mph"
          accent="green"
        />

        <MetricCard
          label="Battery"
          value={telemetry.battery.toFixed(1)}
          unit="%"
          accent="purple"
        />

        <MetricCard
          label="Temperature"
          value={telemetry.temperature.toFixed(1)}
          unit="°C"
          accent="orange"
        />
      </section>
      
      <section className="trendSection">
        <div className="sectionHeading">
          <div>
            <p className="eyebrow">TELEMETRY HISTORY</p>
            <h2>Flight Trends</h2>
          </div>

          <p>Values across recent incoming telemetry messages</p>
        </div>

        <div className="trendGrid">
          <LineChart
            title="Altitude"
            unit="ft"
            color="#38bdf8"
            dataKey="altitude"
            telemetryHistory={mockTelemetryHistory}
          />

          <LineChart
            title="Airspeed"
            unit="mph"
            color="#22c55e"
            dataKey="speed"
            telemetryHistory={mockTelemetryHistory}
          />

          <LineChart
            title="Battery"
            unit="%"
            color="#a78bfa"
            dataKey="battery"
            telemetryHistory={mockTelemetryHistory}
          />

          <LineChart
            title="Temperature"
            unit="°C"
            color="#fb923c"
            dataKey="temperature"
            telemetryHistory={mockTelemetryHistory}
          />
        </div>
      </section>

      <section className="lowerGrid">
        <article className="panel">
          <div className="panelHeader">
            <div>
              <p className="eyebrow">SYSTEM STATUS</p>
              <h2>Aircraft Health</h2>
            </div>

            <span
              className={
                telemetry.status === "NORMAL"
                  ? "statusBadge normal"
                  : "statusBadge warning"
              }
            >
              {telemetry.status}
            </span>
          </div>

          <div className="healthList">
            <div className="healthRow">
              <span>Flight controls</span>
              <strong className="normalText">Operational</strong>
            </div>

            <div className="healthRow">
              <span>Telemetry connection</span>
              <strong className="normalText">Receiving</strong>
            </div>

            <div className="healthRow">
              <span>Power system</span>
              <strong className="normalText">Normal</strong>
            </div>

            <div className="healthRow">
              <span>Temperature</span>
              <strong className="normalText">Normal</strong>
            </div>
          </div>
        </article>

        <article className="panel">
          <div className="panelHeader">
            <div>
              <p className="eyebrow">ACTIVE EVENTS</p>
              <h2>Warnings</h2>
            </div>

            <span className="warningCount">
              {telemetry.warnings.length}
            </span>
          </div>

          {hasWarnings ? (
            <ul className="warningList">
              {telemetry.warnings.map((warning) => (
                <li key={warning}>{warning}</li>
              ))}
            </ul>
          ) : (
            <div className="emptyWarnings">
              <div className="checkmark">✓</div>
              <p>No active warnings</p>
              <span>All monitored systems are within normal ranges.</span>
            </div>
          )}
        </article>
      </section>
    </main>
  );
}

export default App;