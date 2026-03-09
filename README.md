# kubernetes-einkaufsliste
kleines projekt um kubernetes mit docker zu lernen

Eine einfache Web-Anwendung für eine Einkaufsliste, die in einem Kubernetes Pod mit nginx läuft.

# Übersicht

Ein Kleines Projekt wo man eine z.b. Einkaufsliste nimmt mit einem kleinen button der mit javascript zu der einkaufsliste mehr Lebensmittel Hinzufügt
und diese Seite wird über nginx in einem kubernetes pod bereitgestellt.

# Dateien

- `einkaufsliste-http.yaml` - ConfigMap mit HTML-Inhalt
- `einkaufsliste-pod.yaml` - Pod-Definition 

# Voraussetzungen

Docker Instaliert und Läuft im Hintergrund z.b Docker Desktop ist im Hintergrund offen 
Kind(Kubernetes in Docker) instaliert

1 schritt 
   ```bash
   kind create cluster
   ```

2 schritt 
   ```bash
   kubectl apply -f einkaufsliste-http.yaml
  ```

3 schritt 
   ```bash
   kubectl apply -f einkaufsliste-pod.yaml
   ```

4 schritt
   ```bash
   kubectl get pods
   kubectl get configmaps
   ```

5 schritt
   ```bash
   kubectl describe pod mein-pod
   ```

Für Port Forwarding
```bash
kubectl port-forward pod/mein-pod 8080:80
```


webseite Öffnen:
http://localhost:8080


Mikas










