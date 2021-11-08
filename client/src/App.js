import { useEffect, useState } from "react";
import {
  Box,
  Button,
  CssBaseline,
  IconButton,
  List,
  ListItem,
  ListItemText,
  Paper,
  Stack,
  Typography,
} from "@mui/material/";
import DeleteIcon from "@mui/icons-material/Delete";
import { unzip } from "unzipit";

const App = () => {
  const [files, setFiles] = useState([]);
  const [dbPhotos, setDbPhotos] = useState([]);

  const handleFiles = (e) => {
    e.preventDefault();
    setFiles((prev) => {
      prev.forEach((file) => {
        URL.revokeObjectURL(file.url);
      });
      const files = Array.from(e.target.files);
      files.forEach((file) => {
        file.url = URL.createObjectURL(file);
      });
      return files;
    });
  };

  const handleDelete = (url) => {
    setFiles((prev) => {
      return prev.filter((file) => {
        return file.url !== url;
      });
    });
    URL.revokeObjectURL(url);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    files.forEach((file, i) => {
      formData.append(`photos_${i}`, files[i]);
    });
    const response = await fetch("http://localhost:5000/images", {
      method: "POST",
      body: formData,
    });
    if (response.ok) {
      setFiles([]);
    }
  };

  useEffect(() => {
    const fetchDbPhotos = async () => {
      const { entries } = await unzip("http://localhost:5000/images");
      const photos = await Promise.all(
        Object.entries(entries).map(async ([name, entry]) => {
          const blob = await entry.blob();
          const description = name.split("/");
          return {
            name: description[description.length - 1],
            url: URL.createObjectURL(blob),
          };
        })
      );
      setDbPhotos(photos);
    };
    return fetchDbPhotos();
  }, []);

  return (
    <>
      <CssBaseline />
      <Box
        sx={{
          bgcolor: "background.paper",
          display: "flex",
          justifyContent: "space-around",
        }}
      >
        <Box>
          <Stack
            direction="row"
            spacing={2}
            justifyContent="center"
            sx={{ my: 2 }}
          >
            <label htmlFor="contained-button-file">
              <input
                accept="image/*"
                id="contained-button-file"
                multiple
                type="file"
                style={{ display: "none" }}
                onChange={handleFiles}
              />
              <Button variant="contained" component="span">
                Upload
              </Button>
            </label>
            <Button
              variant="contained"
              color="success"
              type="submit"
              onClick={handleSubmit}
            >
              Submit
            </Button>
          </Stack>
          <Paper
            elevation={3}
            sx={{ minWidth: 350, minHeight: 500, flexGrow: 1, my: 2 }}
          >
            <List>
              {files.map((file, i) => {
                return (
                  <ListItem
                    key={i}
                    secondaryAction={
                      <IconButton
                        edge="end"
                        aria-label="delete"
                        onClick={() => {
                          handleDelete(file.url);
                        }}
                      >
                        <DeleteIcon />
                      </IconButton>
                    }
                  >
                    <ListItemText>{file.name}</ListItemText>
                    <img
                      src={file.url}
                      alt={file.name}
                      style={{ width: "75px", height: "75px" }}
                    />
                  </ListItem>
                );
              })}
            </List>
          </Paper>
        </Box>
        <Box>
          <Typography variant="h6" gutterBottom textAlign={"center"}>
            DB
          </Typography>
          <Paper
            elevation={3}
            sx={{ minWidth: 350, minHeight: 500, flexGrow: 1, my: 2 }}
          >
            <List>
              {dbPhotos.map((file, i) => {
                return (
                  <ListItem key={i}>
                    <ListItemText>{file.name}</ListItemText>
                    <img
                      src={file.url}
                      alt={file.name}
                      style={{ width: "75px", height: "75px" }}
                    />
                  </ListItem>
                );
              })}
            </List>
          </Paper>
        </Box>
      </Box>
    </>
  );
};

export default App;
