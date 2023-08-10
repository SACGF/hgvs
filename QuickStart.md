 ```
docker build . -t hgvs
docker run -p 8000:8000 hgvs
```

```sh
curl http://localhost:8000/translate?value=NM_000352.3:c.215A%3EG
```
