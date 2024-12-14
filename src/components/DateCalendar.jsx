import React from "react";
import "../styles/Dashboard.css";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DateCalendar } from "@mui/x-date-pickers/DateCalendar";
import CssBaseline from "@mui/material/CssBaseline";

function Dashboard() {
  const theme = createTheme({
    palette: {
      mode: "light", // o 'dark' si prefieres tema oscuro
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="dashboard">
        <div className="todo">
          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DateCalendar />
          </LocalizationProvider>
        </div>
      </div>
    </ThemeProvider>
  );
}

export default Dashboard;
