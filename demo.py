if __name__ == "__main__":
    from AleUI import App
    from SCENES.debug import build_dev_scene

    PROFILATORE = 0
    from time import perf_counter; start_time = perf_counter() 

    if PROFILATORE:
        import yappi
        yappi.start()


    app: App = App(debug=True)
    app.launch()
    app = build_dev_scene(app)

    while app.running:
        app.update()

    if PROFILATORE:
        yappi.stop()
        func_stats = yappi.get_func_stats()
        func_stats.save('profilatore.prof', type='pstat')    

    print(f"Il programma è stato in esecuzione per {perf_counter() - start_time:.0f}s")