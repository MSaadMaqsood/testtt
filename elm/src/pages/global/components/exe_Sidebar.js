import React from "react";
import clsx from "clsx";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import Drawer from "@material-ui/core/Drawer";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import List from "@material-ui/core/List";
import CssBaseline from "@material-ui/core/CssBaseline";
import Typography from "@material-ui/core/Typography";
import Divider from "@material-ui/core/Divider";
import IconButton from "@material-ui/core/IconButton";
import MenuIcon from "@material-ui/icons/Menu";
import ChevronLeftIcon from "@material-ui/icons/ChevronLeft";
import ChevronRightIcon from "@material-ui/icons/ChevronRight";
import ListItem from "@material-ui/core/ListItem";
import GroupIcon from "@material-ui/icons/Group";
import AddIcon from "@material-ui/icons/Add";
import ExitToAppIcon from "@material-ui/icons/ExitToApp";
import LoopIcon from "@material-ui/icons/Loop";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import DescriptionIcon from "@material-ui/icons/Description";
import ListItemText from "@material-ui/core/ListItemText";
import HomeIcon from "@material-ui/icons/Home";
import CloudIcon from "@material-ui/icons/Cloud";
import CodeIcon from "@material-ui/icons/Code";
import { ListNested } from "react-bootstrap-icons";

const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    paddingTop: "150px",
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    backgroundColor: "black",
    transition: theme.transitions.create(["width", "margin"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(["width", "margin"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  menuButton: {
    // marginTop: 50,
    marginRight: 36,
  },
  marginAutoItem: {
    margin: "auto",
  },

  marginRightItem: {
    paddingRight: "10px",
  },
  hide: {
    display: "none",
  },
  drawer: {
    // marginTop: 50,
    width: drawerWidth,
    flexShrink: 0,
    whiteSpace: "nowrap",
  },
  drawerOpen: {
    marginTop: 70,
    width: drawerWidth,
    transition: theme.transitions.create("width", {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  toolBarIconsLeft: {
    justifyContent: "space-between",
  },
  accrow: {
    float: "right",
  },
  accrow_width: {
    width: "100%",
  },
  drawerClose: {
    marginTop: 70,
    transition: theme.transitions.create("width", {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    overflowX: "hidden",
    width: theme.spacing(7) + 1,
    [theme.breakpoints.up("sm")]: {
      width: theme.spacing(9) + 1,
    },
  },
  toolbar: {
    display: "flex",
    alignItems: "center",
    justifyContent: "flex-end",
    padding: theme.spacing(0, 1),
    // necessary for content to be below app bar
    ...theme.mixins.toolbar,
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
  },
}));

export default function Exe_MiniDrawer() {
  const classes = useStyles();
  const theme = useTheme();
  const [open, setOpen] = React.useState(false);

  const handleDrawerOpen = () => {
    setOpen(!open);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  return (
    <div>
      <Drawer
        variant="permanent"
        className={clsx(classes.drawer, {
          [classes.drawerOpen]: open,
          [classes.drawerClose]: !open,
        })}
        classes={{
          paper: clsx({
            [classes.drawerOpen]: open,
            [classes.drawerClose]: !open,
          }),
        }}
      >
        <List>
          <ListItem button>
            <ListItemIcon>
              <IconButton
                color="inherit"
                aria-label="open drawer"
                onClick={handleDrawerOpen}
                edge="start"
                className={clsx(classes.menuButton)}
              >
                <MenuIcon />
              </IconButton>
            </ListItemIcon>
            <ListItemText> </ListItemText>
          </ListItem>
          <ListItem button>
            <ListItemIcon
              onClick={() => {
                window.location.href = "/exe_dashboard";
              }}
            >
              <HomeIcon />
            </ListItemIcon>
            <ListItemText
              primary="Home"
              onClick={() => {
                window.location.href = "/exe_dashboard";
              }}
            />
          </ListItem>
          <ListItem button>
            <ListItemIcon
              onClick={() => {
                window.location.href = "/exe_allviolations";
              }}
            >
              <DescriptionIcon />
            </ListItemIcon>
            <ListItemText
              primary="All Violations"
              onClick={() => {
                window.location.href = "/exe_allviolations";
              }}
            />
          </ListItem>
         
          
          {/* <ListItem button>
            <ListItemIcon>
              <CodeIcon  onClick={() =>{  window.location.href ="/map_api";  }}/>
            </ListItemIcon>
            <ListItemText primary="Map API"  onClick={() =>{  window.location.href ="/map_api";  }}/>
          </ListItem> */}
        </List>
      </Drawer>
      <main className={classes.content}>
        <div className={classes.toolbar} />
        <Typography paragraph></Typography>
      </main>
    </div>
  );
}
